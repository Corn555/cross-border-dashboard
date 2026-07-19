"""页面：分析概览 — KPI 卡片、客户分层、排行表格、交互式筛选。"""
import streamlit as st

from src.ui.components import country_filter, kpi_row, require_result, top_n_slider


def show():
    st.header("分析概览")
    result = require_result()
    if result is None:
        return

    sales = result.sales_result
    customers = result.customer_result

    # ── KPI 栏 ──
    kpi_row([
        ("总营收", f"${sales.total_revenue:,.0f}"),
        ("总订单数", f"{sales.total_orders:,}"),
        ("总客户数", f"{sales.total_customers:,}"),
        ("平均客单价", f"${sales.avg_order_value:,.0f}"),
    ])

    st.divider()

    # ── 客户分层 ──
    st.subheader("客户价值分层（RFM 模型）")
    seg = customers.segment_stats
    total = sum(seg.values())
    kpi_row([
        ("高价值客户", f"{seg.get('高价值客户', 0):,}", f"{seg.get('高价值客户', 0) / total * 100:.1f}%"),
        ("中价值客户", f"{seg.get('中价值客户', 0):,}", f"{seg.get('中价值客户', 0) / total * 100:.1f}%"),
        ("低价值客户", f"{seg.get('低价值客户', 0):,}", f"{seg.get('低价值客户', 0) / total * 100:.1f}%"),
    ])

    st.divider()

    # ── 筛选控件 ──
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        n = top_n_slider(default=10, max_n=30)
    with col_f2:
        selected_countries = country_filter(result)

    # ── Top 商品 ──
    st.subheader(f"Top {n} 商品（按营收）")
    top_p = sales.top_products.head(n).reset_index(drop=True)
    st.dataframe(top_p, use_container_width=True)

    # ── Top 国家 ──
    st.subheader(f"Top {n} 国家（按营收）")
    top_c = sales.top_countries.copy()
    if selected_countries:
        top_c = top_c[top_c["Country"].isin(selected_countries)]
    top_c = top_c.head(n).reset_index(drop=True)
    st.dataframe(top_c, use_container_width=True)

    # ── 月度营收明细 ──
    st.divider()
    st.subheader("月度营收明细")
    monthly = sales.monthly_revenue.copy()
    monthly["Month"] = monthly["Month"].dt.strftime("%Y-%m")
    monthly["Revenue"] = monthly["Revenue"].apply(lambda v: f"${v:,.0f}")
    st.dataframe(monthly, use_container_width=True)
