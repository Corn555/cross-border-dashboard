"""
模块：客户分析器
职责：RFM 客户分层、客户地理分布分析。
"""
import pandas as pd


def analyze_customers(df: pd.DataFrame, reference_date: pd.Timestamp | None = None) -> dict:
    """
    基于清洗后的交易数据执行 RFM 分析和客户地理分布统计。

    RFM 模型：
    - R（Recency）：距最后一次购买的天数（越小越好）
    - F（Frequency）：独立订单数（越多越好）
    - M（Monetary）：总消费金额（越高越好）
    每项按四分位数打分 1-4，组合为 RFM 分数，再划分为高/中/低价值客户。

    Args:
        df: 清洗后的 DataFrame（需包含 Customer ID, InvoiceDate,
            Invoice, TotalSales, Country 列）。
        reference_date: RFM 参考日期，默认为数据中最后一天 + 1 天。

    Returns:
        dict，包含：rfm_table (DataFrame), segments (dict 分层统计),
        customers_by_country (DataFrame)。
    """
    if reference_date is None:
        reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    # --- RFM 计算 ---
    rfm = df.groupby("Customer ID").agg(
        Recency=("InvoiceDate", lambda x: (reference_date - x.max()).days),
        Frequency=("Invoice", "nunique"),
        Monetary=("TotalSales", "sum"),
    ).reset_index()

    # 百分位排名打分（1-4，4 最好）
    # 用 rank(pct) 代替 qcut，避免因大量重复值导致分位边界不唯一而报错
    r_pct = rfm["Recency"].rank(pct=True)
    f_pct = rfm["Frequency"].rank(pct=True)
    m_pct = rfm["Monetary"].rank(pct=True)

    # Recency 越低越好 → 排名越高分越高
    rfm["R_Score"] = pd.cut(r_pct, bins=[0, 0.25, 0.5, 0.75, 1.0],
                            labels=[4, 3, 2, 1]).astype(int)
    # Frequency 越高越好 → 排名越高分越高
    rfm["F_Score"] = pd.cut(f_pct, bins=[0, 0.25, 0.5, 0.75, 1.0],
                            labels=[1, 2, 3, 4]).astype(int)
    # Monetary 越高越好 → 排名越高分越高
    rfm["M_Score"] = pd.cut(m_pct, bins=[0, 0.25, 0.5, 0.75, 1.0],
                            labels=[1, 2, 3, 4]).astype(int)

    # 组合 RFM 分数
    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(str)
        + rfm["F_Score"].astype(str)
        + rfm["M_Score"].astype(str)
    )

    # 客户分层
    def _segment(rfm_row):
        r, f, m = int(rfm_row["R_Score"]), int(rfm_row["F_Score"]), int(rfm_row["M_Score"])
        if r >= 3 and f >= 3 and m >= 3:
            return "高价值客户"
        elif r >= 3 or f >= 3 or m >= 3:
            return "中价值客户"
        else:
            return "低价值客户"

    rfm["Segment"] = rfm.apply(_segment, axis=1)

    segment_stats = rfm["Segment"].value_counts().to_dict()

    # --- 客户地理分布 ---
    customers_by_country = (
        df.groupby("Country")["Customer ID"]
        .nunique()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    customers_by_country.columns = ["Country", "Customers"]

    # --- Top 10 高价值客户 ---
    top_customers = rfm.nlargest(10, "Monetary")[
        ["Customer ID", "Recency", "Frequency", "Monetary", "Segment"]
    ]

    result = {
        "rfm_table": rfm,
        "segment_stats": segment_stats,
        "customers_by_country": customers_by_country,
        "top_customers": top_customers,
        "total_customers": len(rfm),
    }

    # --- 打印客户分析报告 ---
    print("\n" + "=" * 56)
    print("  客户分析报告（RFM 模型）")
    print("=" * 56)
    print(f"  总客户数           : {len(rfm):>12,}")
    print("-" * 56)
    print("  客户价值分层")
    for seg in ["高价值客户", "中价值客户", "低价值客户"]:
        count = segment_stats.get(seg, 0)
        pct = count / len(rfm) * 100
        print(f"  {seg:<16s}: {count:>10,}  ({pct:>5.1f}%)")
    print("-" * 56)
    print("  高价值客户 Top 5（按消费额）")
    for _, row in top_customers.head(5).iterrows():
        cid = int(row["Customer ID"])
        print(f"  客户 {cid:>6d}  |  最近 {int(row['Recency']):>4d}天  "
              f" 订单 {int(row['Frequency']):>4d}  |  $ {row['Monetary']:>10,.0f}")
    print("-" * 56)
    print("  Top 5 国家（按客户数）")
    for _, row in customers_by_country.head(5).iterrows():
        print(f"  {row['Country']:<30s} {int(row['Customers']):>10,} 位客户")
    print("=" * 56 + "\n")

    return result
