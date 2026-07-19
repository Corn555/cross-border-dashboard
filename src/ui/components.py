"""
可复用的 Streamlit UI 组件。

包含：Pipeline 执行、KPI 卡片、数据校验、过滤器。
"""
import time

import pandas as pd
import streamlit as st

from src.exceptions import ProjectError
from src.logger import get_logger
from src.pipeline import run_pipeline

_LOGGER = get_logger(__name__)

# CSV 上传必须包含的关键列
_REQUIRED_COLUMNS = ["Invoice", "StockCode", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country", "Description"]


def run_pipeline_with_ui(raw_path, processed_path, charts_dir, report_path):
    """执行 Pipeline，带 spinner、计时和错误处理。"""
    with st.spinner("正在运行分析流程（6 个阶段）..."):
        try:
            t0 = time.perf_counter()
            result = run_pipeline(
                raw_data_path=raw_path,
                processed_data_path=processed_path,
                charts_output_dir=charts_dir,
                report_output_path=report_path,
            )
            elapsed = time.perf_counter() - t0
            st.session_state.pipeline_result = result
            st.session_state.last_run_elapsed = elapsed
            st.success(f"分析完成！耗时 {elapsed:.1f} 秒。请前往其它页面查看结果。")
            st.balloons()
        except ProjectError as e:
            st.error(f"流程执行失败: {e}")
            _LOGGER.exception("Pipeline failed")


def require_result():
    """Guard: 若尚未运行分析，显示 warning 并返回 None。"""
    result = st.session_state.get("pipeline_result")
    if result is None:
        st.warning("请先在「数据上传」页面运行分析", icon="⚠️")
    return result


def kpi_row(metrics):
    """渲染一行 KPI 卡片。metrics = [(label, value, delta?), ...]"""
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        label, value = m[0], m[1]
        delta = m[2] if len(m) > 2 else None
        col.metric(label, value, delta=delta)


def validate_csv(uploaded_file) -> list[str] | None:
    """
    校验上传的 CSV 文件。

    Returns:
        缺失的必需列名列表；若全部满足则返回 None。
    """
    try:
        raw = uploaded_file.getvalue()
        # 尝试 latin1 编码（与 data_loader 保持一致）
        try:
            df = pd.read_csv(pd.io.common.BytesIO(raw), encoding="latin1", nrows=0)
        except Exception:
            df = pd.read_csv(pd.io.common.BytesIO(raw), encoding="utf-8", nrows=0)
        missing = [c for c in _REQUIRED_COLUMNS if c not in df.columns]
        return missing if missing else None
    except Exception as e:
        return [f"无法解析 CSV: {e}"]


def country_filter(result, key="country_filter"):
    """渲染国家多选过滤器，返回选中的国家列表。"""
    countries = list(result.sales_result.top_countries["Country"])
    return st.multiselect(
        "国家筛选",
        options=countries,
        default=countries[:5],
        key=key,
    )


def top_n_slider(default=10, max_n=50, key="top_n"):
    """渲染 Top N 滑块，返回选中的 N 值。"""
    return st.slider("显示 Top N", min_value=5, max_value=max_n, value=default, step=5, key=key)
