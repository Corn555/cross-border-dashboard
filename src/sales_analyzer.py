"""
模块：销售分析器
职责：计算销售核心指标——总营收、月度趋势、热销商品、国家分布、客单价。
"""
import pandas as pd


def analyze_sales(df: pd.DataFrame) -> dict:
    """
    基于清洗后的数据计算所有销售 KPI。

    Args:
        df: 清洗后的 DataFrame（需包含 TotalSales, InvoiceDate,
            Description, Country, Invoice 列）。

    Returns:
        dict，包含：total_revenue, total_orders, avg_order_value,
        total_customers, monthly_revenue (DataFrame),
        top_products (DataFrame), top_countries (DataFrame)。
    """
    total_revenue = float(df["TotalSales"].sum())
    total_orders = int(df["Invoice"].nunique())
    total_customers = int(df["Customer ID"].nunique())
    avg_order_value = total_revenue / total_orders if total_orders else 0.0

    # 月度营收趋势
    monthly_revenue = (
        df.set_index("InvoiceDate")
        .resample("ME")["TotalSales"]
        .sum()
        .reset_index()
    )
    monthly_revenue.columns = ["Month", "Revenue"]

    # Top 10 商品（按营收）
    top_products = (
        df.groupby("Description")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_products.columns = ["Product", "Revenue"]

    # Top 10 国家（按营收）
    top_countries = (
        df.groupby("Country")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_countries.columns = ["Country", "Revenue"]

    # Top 10 国家（按订单数）
    top_countries_orders = (
        df.groupby("Country")["Invoice"]
        .nunique()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_countries_orders.columns = ["Country", "Orders"]

    result = {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "avg_order_value": avg_order_value,
        "monthly_revenue": monthly_revenue,
        "top_products": top_products,
        "top_countries": top_countries,
        "top_countries_orders": top_countries_orders,
    }

    # --- 打印销售分析摘要 ---
    print("\n" + "=" * 56)
    print("  销售分析报告")
    print("=" * 56)
    print(f"  总营收（$）        : $ {total_revenue:>12,.2f}")
    print(f"  总订单数           :   {total_orders:>12,}")
    print(f"  总客户数           :   {total_customers:>12,}")
    print(f"  平均客单价（$）    : $ {avg_order_value:>12,.2f}")
    print("-" * 56)
    print("  Top 5 商品（按营收）")
    for _, row in top_products.head(5).iterrows():
        desc = str(row["Product"])[:38]
        print(f"  {desc:<38s} $ {row['Revenue']:>10,.0f}")
    print("-" * 56)
    print("  Top 5 国家（按营收）")
    for _, row in top_countries.head(5).iterrows():
        print(f"  {row['Country']:<38s} $ {row['Revenue']:>10,.0f}")
    print("=" * 56 + "\n")

    return result
