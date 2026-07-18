"""
模块：src.config
职责：集中管理所有可配置参数。

用法：
    from src.config import RAW_DATA_PATH, VERSION
"""

from .config import (
    CHART_DPI,
    CHART_FIGURE_SIZE,
    CHARTS_OUTPUT_DIR,
    PROCESSED_DATA_DIR,
    PROCESSED_DATA_PATH,
    PROJECT_NAME,
    RAW_DATA_PATH,
    REPORT_OUTPUT_PATH,
    REPORTS_OUTPUT_DIR,
    VERSION,
)

__all__ = [
    "PROJECT_NAME",
    "VERSION",
    "RAW_DATA_PATH",
    "PROCESSED_DATA_DIR",
    "PROCESSED_DATA_PATH",
    "CHARTS_OUTPUT_DIR",
    "REPORTS_OUTPUT_DIR",
    "REPORT_OUTPUT_PATH",
    "CHART_FIGURE_SIZE",
    "CHART_DPI",
]
