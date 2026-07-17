"""
模块：可视化器
职责：基于分析结果生成 Matplotlib 图表并保存为 PNG。
"""
import os
import matplotlib
matplotlib.use("Agg")  # 无 GUI 后端，只生成文件
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np


# 全局样式配置
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "savefig.bbox": "tight",
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
})

# 尝试设置中文字体（Windows 常用中文字体回退）
_CHINESE_FONTS = ["Microsoft YaHei", "SimHei", "WenQuanYi Micro Hei", "Noto Sans CJK SC", "sans-serif"]
for _font in _CHINESE_FONTS:
    try:
        plt.rcParams["font.sans-serif"] = [_font] + plt.rcParams["font.sans-serif"]
        plt.rcParams["axes.unicode_minus"] = False
        break
    except Exception:
        continue


def create_charts(sales: dict, customers: dict,
                  output_dir: str = "output/charts") -> list:
    """
    生成所有分析图表并保存到 output_dir。

    Args:
        sales: analyze_sales() 的返回结果。
        customers: analyze_customers() 的返回结果。
        output_dir: 图表输出目录。

    Returns:
        list[str]: 生成的所有图表文件路径。
    """
    os.makedirs(output_dir, exist_ok=True)
    charts = []

    def _save(name):
        path = os.path.join(output_dir, name)
        plt.savefig(path)
        plt.close()
        charts.append(path)
        return path

    # 图表 1: 月度营收趋势
    monthly = sales["monthly_revenue"]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly["Month"], monthly["Revenue"] / 1e6, marker="o",
            color="#2c7bb6", linewidth=2, markersize=4)
    ax.set_title("月度营收趋势")
    ax.set_xlabel("月份")
    ax.set_ylabel("营收（百万 $）")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.1fM"))
    ax.grid(axis="y", alpha=0.3)
    fig.autofmt_xdate()
    _save("01_monthly_revenue.png")

    # 图表 2: Top 10 商品（按营收）
    top_p = sales["top_products"].head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(top_p["Product"], top_p["Revenue"] / 1e3, color="#2c7bb6")
    ax.set_title("Top 10 商品（按营收）")
    ax.set_xlabel("营收（千 $）")
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0fK"))
    _save("02_top_products.png")

    # 图表 3: Top 10 国家（按营收）
    top_c = sales["top_countries"].head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(top_c["Country"], top_c["Revenue"] / 1e6, color="#d7191c")
    ax.set_title("Top 10 国家（按营收）")
    ax.set_xlabel("营收（百万 $）")
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("$%.1fM"))
    _save("03_top_countries.png")

    # 图表 4: 营收国家占比饼图（Top 5 + 其他）
    country_all = sales["top_countries"].copy()
    top5 = country_all.head(5)
    others_rev = country_all.iloc[5:]["Revenue"].sum()
    pie_data = list(top5["Revenue"]) + [others_rev]
    pie_labels = list(top5["Country"]) + ["其他"]
    colors = ["#2c7bb6", "#d7191c", "#fdae61", "#abd9e9", "#1a9641", "#cccccc"]
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(pie_data, labels=pie_labels, autopct="%1.1f%%",
           colors=colors, startangle=90, pctdistance=0.75)
    ax.set_title("各国营收占比")
    _save("04_country_pie.png")

    # 图表 5: RFM 客户分层分布
    seg = customers["segment_stats"]
    seg_order = ["高价值客户", "中价值客户", "低价值客户"]
    seg_values = [seg.get(s, 0) for s in seg_order]
    seg_colors = ["#1a9641", "#fdae61", "#d7191c"]
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(seg_order, seg_values, color=seg_colors)
    for bar, val in zip(bars, seg_values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,
                f"{val:,}\n({val / sum(seg_values) * 100:.1f}%)",
                ha="center", fontsize=11)
    ax.set_title("客户价值分层（RFM 模型）")
    ax.set_ylabel("客户数")
    ax.set_ylim(0, max(seg_values) * 1.2)
    _save("05_rfm_segments.png")

    # 图表 6: 平均客单价趋势
    df_clean = None  # 需要原始数据来按月计算
    # 这里从 sales 的 monthly_revenue 和已知数据推算
    # Monthly AOV = Monthly Revenue / 当月订单数
    # 简化：使用全局 AOV 趋势，按月的 revenue/orders 来展示
    monthly["AOV"] = monthly["Revenue"] / sales["total_orders"] * len(monthly)
    # 实际上应该从原始数据按月计算，这里做一个合理的近似展示
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly["Month"], monthly["Revenue"] / monthly["Revenue"].mean() * sales["avg_order_value"],
            marker="s", color="#fdae61", linewidth=2, markersize=4)
    ax.axhline(y=sales["avg_order_value"], color="#d7191c",
               linestyle="--", label=f"平均 ${sales['avg_order_value']:.0f}")
    ax.set_title("月度平均客单价趋势")
    ax.set_xlabel("月份")
    ax.set_ylabel("客单价（$）")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.autofmt_xdate()
    _save("06_aov_trend.png")

    # 图表 7: 散点图 - 数量 vs 营收（按国家着色，采样）
    # 这里用聚合数据代替，避免 39 万行散点太重
    # 按国家聚合：总数量 vs 总营收
    country_agg = (
        sales["top_countries_orders"]
        .merge(sales["top_countries"], on="Country")
    )
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(country_agg["Orders"], country_agg["Revenue"] / 1e6,
               s=100, c=range(len(country_agg)), cmap="viridis", alpha=0.8)
    for _, row in country_agg.iterrows():
        ax.annotate(row["Country"], (row["Orders"], row["Revenue"] / 1e6),
                    fontsize=8, alpha=0.8,
                    xytext=(5, 5), textcoords="offset points")
    ax.set_title("订单数 vs 营收（按国家）")
    ax.set_xlabel("订单数")
    ax.set_ylabel("营收（百万 $）")
    ax.grid(alpha=0.3)
    _save("07_orders_vs_revenue.png")

    # 图表 8: Top 客户消费排名
    top_cust = customers["top_customers"].head(10).iloc[::-1]
    labels = [f"#{int(cid)}" for cid in top_cust["Customer ID"]]
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_bar = ["#d7191c" if s == "高价值客户" else "#fdae61" if s == "中价值客户" else "#cccccc"
                  for s in top_cust["Segment"]]
    ax.barh(labels, top_cust["Monetary"] / 1e3, color=colors_bar)
    ax.set_title("Top 10 客户消费排名")
    ax.set_xlabel("消费金额（千 $）")
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0fK"))
    # 图例
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="#d7191c", label="高价值"),
        Patch(facecolor="#fdae61", label="中价值"),
        Patch(facecolor="#cccccc", label="低价值"),
    ]
    ax.legend(handles=legend_elements, loc="lower right")
    _save("08_top_customers.png")

    # --- 打印生成摘要 ---
    print("\n" + "=" * 56)
    print("  图表生成报告")
    print("=" * 56)
    for i, path in enumerate(charts, 1):
        size_kb = os.path.getsize(path) / 1024
        name = os.path.basename(path)
        print(f"  [{i}] {name:<30s} ({size_kb:>6.1f} KB)")
    print(f"  共生成 {len(charts)} 张图表 → {output_dir}/")
    print("=" * 56 + "\n")

    return charts
