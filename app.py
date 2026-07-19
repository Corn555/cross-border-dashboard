"""
app.py — Streamlit 展示层入口。

职责：初始化 Streamlit + 路由页面。不包含任何 UI 组件或业务逻辑。
"""
import sys

import streamlit as st

from src.config import load_config
from src.logger import get_logger, setup_logging
from src.ui import about, analysis, charts, report, upload

_LOGGER = get_logger(__name__)

st.set_page_config(
    page_title="跨境电商销售数据分析平台",
    page_icon="📊",
    layout="wide",
)

if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None
if "cfg" not in st.session_state:
    st.session_state.cfg = load_config()

_PAGES = {
    "📤 数据上传": upload,
    "📊 分析概览": analysis,
    "📈 图表展示": charts,
    "📄 报告下载": report,
    "ℹ️ 关于": about,
}


def main():
    cfg = st.session_state.cfg
    st.title(cfg["project"]["name"])
    st.caption("Cross-border E-commerce Sales Dashboard")

    page = st.sidebar.radio("导航", list(_PAGES.keys()))
    st.sidebar.divider()
    st.sidebar.caption(f"v{cfg['project']['version']}")

    _PAGES[page].show()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    setup_logging()
    main()
