"""
app.py — Streamlit 展示层入口。

职责：
  1. 提供 Web UI（sidebar + 5 个页面）
  2. 调用现有 run_pipeline()（零改动）
  3. 展示 KPI、图表、报告下载

注意：app.py 不包含任何业务逻辑。所有计算委托给 src/ 模块。
      main.py (CLI) 保持原有行为不变。
"""
import sys
import tempfile
from pathlib import Path

import streamlit as st

from src.config import load_config
from src.exceptions import ProjectError
from src.logger import get_logger, setup_logging
from src.pipeline import run_pipeline

_LOGGER = get_logger(__name__)

st.set_page_config(
    page_title="跨境电商销售数据分析平台",
    page_icon="📊",
    layout="wide",
)

# 初始化 session state
if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None
if "cfg" not in st.session_state:
    st.session_state.cfg = load_config()

_CFG = st.session_state.cfg


def _run(raw_path, processed_path, charts_dir, report_path):
    with st.spinner("正在运行分析流程（6 个阶段）..."):
        try:
            result = run_pipeline(
                raw_data_path=raw_path,
                processed_data_path=processed_path,
                charts_output_dir=charts_dir,
                report_output_path=report_path,
            )
            st.session_state.pipeline_result = result
            st.success("分析完成！请前往「分析概览」「图表展示」「报告下载」查看结果。")
        except ProjectError as e:
            st.error(f"流程执行失败: {e}")
            _LOGGER.exception("Pipeline failed")


# ===========================================================================
# 页面: 数据上传
# ===========================================================================
def _page_upload():
    st.header("数据上传")
    st.markdown("上传 CSV 文件并运行分析流程，或使用项目默认数据。")

    uploaded_file = st.file_uploader("选择 CSV 文件", type=["csv"])

    if uploaded_file is not None:
        st.success(f"已上传: {uploaded_file.name} ({uploaded_file.size:,} bytes)")
        if st.button("运行分析（使用上传文件）", type="primary"):
            tmp = Path(tempfile.mkdtemp())
            raw = tmp / "uploaded.csv"
            raw.write_bytes(uploaded_file.getvalue())
            _run(str(raw), str(tmp / "processed.csv"),
                 str(tmp / "charts"), str(tmp / "report.html"))
    else:
        st.info("请上传一个 CSV 文件开始分析")

    st.divider()
    st.caption("— 或者 —")
    if st.button("运行分析（使用默认数据）"):
        p = _CFG["paths"]
        _run(str(p["raw_data"]), str(p["processed_data"]),
             str(p["charts_dir"]), str(p["report_output"]))


# ===========================================================================
# 页面: 分析概览
# ===========================================================================
def _page_analysis():
    st.header("分析概览")
    result = st.session_state.pipeline_result
    if result is None:
        st.warning("请先在「数据上传」页面运行分析", icon="⚠️")
        return

    sales = result.sales_result
    customers = result.customer_result

    # KPI 卡片
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("总营收", f"${sales.total_revenue:,.0f}")
    c2.metric("总订单数", f"{sales.total_orders:,}")
    c3.metric("总客户数", f"{sales.total_customers:,}")
    c4.metric("平均客单价", f"${sales.avg_order_value:,.0f}")

    st.divider()

    # 客户分层
    st.subheader("客户价值分层（RFM 模型）")
    seg = customers.segment_stats
    total = sum(seg.values())
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("高价值客户", f"{seg.get('高价值客户', 0):,}",
               f"{seg.get('高价值客户', 0) / total * 100:.1f}%")
    sc2.metric("中价值客户", f"{seg.get('中价值客户', 0):,}",
               f"{seg.get('中价值客户', 0) / total * 100:.1f}%")
    sc3.metric("低价值客户", f"{seg.get('低价值客户', 0):,}",
               f"{seg.get('低价值客户', 0) / total * 100:.1f}%")

    st.divider()

    # Top 商品
    st.subheader("Top 10 商品（按营收）")
    top_p = sales.top_products.head(10).reset_index(drop=True)
    st.dataframe(top_p, use_container_width=True)

    st.divider()

    # Top 国家
    st.subheader("Top 10 国家（按营收）")
    top_c = sales.top_countries.head(10).reset_index(drop=True)
    st.dataframe(top_c, use_container_width=True)

    # 月度营收
    st.divider()
    st.subheader("月度营收明细")
    monthly = sales.monthly_revenue.copy()
    monthly["Month"] = monthly["Month"].dt.strftime("%Y-%m")
    monthly["Revenue"] = monthly["Revenue"].apply(lambda v: f"${v:,.0f}")
    st.dataframe(monthly, use_container_width=True)


# ===========================================================================
# 页面: 图表展示
# ===========================================================================
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


def _page_charts():
    st.header("图表展示")
    result = st.session_state.pipeline_result
    if result is None:
        st.warning("请先在「数据上传」页面运行分析", icon="⚠️")
        return

    # 构建 filename -> full_path 映射
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


# ===========================================================================
# 页面: 报告下载
# ===========================================================================
def _page_report():
    st.header("报告下载")
    result = st.session_state.pipeline_result
    if result is None:
        st.warning("请先在「数据上传」页面运行分析", icon="⚠️")
        return

    report_path = result.report_path
    if not report_path.exists():
        st.error(f"报告文件不存在: {report_path}")
        return

    html = report_path.read_text(encoding="utf-8")
    size_kb = report_path.stat().st_size / 1024

    st.download_button(
        label=f"下载 HTML 报告 ({size_kb:.1f} KB)",
        data=html,
        file_name="sales_report.html",
        mime="text/html",
        type="primary",
    )

    st.divider()
    st.subheader("报告预览")
    st.components.v1.html(html, height=800, scrolling=True)


# ===========================================================================
# 页面: 关于
# ===========================================================================
def _page_about():
    st.header("关于本项目")
    proj = _CFG["project"]
    st.markdown(f"""
    ### {proj['name']}

    **版本**: {proj['version']}

    基于 **四层架构** 构建的跨境电商销售数据分析平台：

    ```
    Presentation    main.py (CLI) + app.py (Web)    ← 双入口
    Application     src/pipeline/                    ← 流程编排
    Business        sales/customer analyzer          ← 纯计算
    Data            loader + cleaner                 ← I/O
    Infrastructure  config / logger / exceptions     ← 横切能力
    ```

    **分析能力**:
    - 销售 KPI：总营收、订单数、客单价、月度趋势
    - 商品分析：Top 10 排行、品类洞察
    - 客户分析：RFM 分层（高/中/低价值）
    - 可视化：8 张专业图表
    - 报告：自包含 HTML（base64 内嵌图片）

    **技术栈**: Python 3.12+, Pandas, Matplotlib, Streamlit
    """)


# ===========================================================================
# Router
# ===========================================================================
_PAGES = {
    "📤 数据上传": _page_upload,
    "📊 分析概览": _page_analysis,
    "📈 图表展示": _page_charts,
    "📄 报告下载": _page_report,
    "ℹ️ 关于": _page_about,
}


def main():
    st.title(_CFG["project"]["name"])
    st.caption("Cross-border E-commerce Sales Dashboard")

    page = st.sidebar.radio("导航", list(_PAGES.keys()))
    st.sidebar.divider()
    st.sidebar.caption(f"版本: {_CFG['project']['version']}")

    _PAGES[page]()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    setup_logging()
    main()
