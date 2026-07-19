"""页面：报告下载 — HTML 预览 + 下载按钮。"""
import streamlit as st

from src.ui.components import require_result


def show():
    st.header("报告下载")
    result = require_result()
    if result is None:
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
    st.info(f"报告大小: {size_kb:.1f} KB，内容较长，可滚动查看。")
    st.components.v1.html(html, height=800, scrolling=True)
