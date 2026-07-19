"""页面：数据上传。"""
import tempfile
from pathlib import Path

import streamlit as st

from src.ui.components import run_pipeline_with_ui, validate_csv


def show():
    st.header("数据上传")
    st.markdown("上传 CSV 文件并运行分析流程，或使用项目默认数据。")

    uploaded_file = st.file_uploader("选择 CSV 文件（.csv）", type=["csv"])

    if uploaded_file is not None:
        st.info(f"文件名: {uploaded_file.name}  |  大小: {uploaded_file.size / 1024:.1f} KB")

        missing = validate_csv(uploaded_file)
        if missing:
            st.error(f"CSV 缺少以下必需列: {', '.join(missing)}")
        else:
            st.success("CSV 格式校验通过 ✓")
            if st.button("运行分析（使用上传文件）", type="primary"):
                tmp = Path(tempfile.mkdtemp())
                raw = tmp / "uploaded.csv"
                raw.write_bytes(uploaded_file.getvalue())
                run_pipeline_with_ui(
                    str(raw), str(tmp / "processed.csv"),
                    str(tmp / "charts"), str(tmp / "report.html"),
                )
    else:
        st.info("请上传一个 CSV 文件，文件需包含以下列: Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country")

    st.divider()
    st.caption("— 或者使用项目自带的默认数据 —")
    if st.button("运行分析（使用默认数据）"):
        cfg = st.session_state.cfg
        p = cfg["paths"]
        run_pipeline_with_ui(
            str(p["raw_data"]), str(p["processed_data"]),
            str(p["charts_dir"]), str(p["report_output"]),
        )

    # 显示上次运行耗时
    elapsed = st.session_state.get("last_run_elapsed")
    if elapsed:
        st.caption(f"上次运行耗时: {elapsed:.1f} 秒")
