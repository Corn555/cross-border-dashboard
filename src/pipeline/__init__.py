"""
模块：src.pipeline
职责：Application Layer — 编排完整数据分析流程。

用法：
    from src.pipeline import run_pipeline

    result = run_pipeline(
        raw_data_path="data/raw/sales.csv",
        processed_data_path="data/processed/sales_clean.csv",
        charts_output_dir="output/charts",
        report_output_path="output/reports/report.html",
    )
"""

from .pipeline import run_pipeline

__all__ = ["run_pipeline"]
