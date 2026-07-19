"""页面：图表展示 — 2 列网格布局。"""
from pathlib import Path

import streamlit as st

from src.ui.components import require_result

_CHART_TITLES = [
    ("月度营收趋势", "01_monthly_revenue.png"),
    ("Top 10 商品（按营收）", "02_top_products.png"),
    ("Top 10 国家（按营收）", "03_top_countries.png"),
    ("各国营收占比（饼图）", "04_country_pie.png"),
    ("客户价值分层（RFM）", "05_rfm_segments.png"),
    ("月度平均客单价趋势", "06_aov_trend.png"),
    ("订单数 vs 营收（散点）", "07_orders_vs_revenue.png"),
    ("Top 10 客户消费排名", "08_top_customers.png"),
]


def show():
    st.header("图表展示")
    result = require_result()
    if result is None:
        return

    chart_map = {Path(p).name: p for p in result.charts}

    for i in range(0, len(_CHART_TITLES), 2):
        cols = st.columns(2)
        for j in range(2):
            idx = i + j
            if idx >= len(_CHART_TITLES):
                break
            title, filename = _CHART_TITLES[idx]
            with cols[j]:
                st.subheader(title)
                if filename in chart_map:
                    st.image(chart_map[filename], use_container_width=True)
                else:
                    st.caption("（图表未生成）")
