"""
模块：配置加载器
职责：从 YAML 文件加载配置，缺失时回退到 Python 默认值。
"""
from pathlib import Path

import yaml

from . import config as _defaults


def load_config(path: str | Path = "config/config.yaml") -> dict:
    """
    加载 YAML 配置文件，缺失时使用 Python 默认值。

    Args:
        path: YAML 配置文件路径。

    Returns:
        dict: 合并后的完整配置。
    """
    yaml_data = _read_yaml(path)
    return _merge(yaml_data)


def _read_yaml(path: str | Path) -> dict:
    """读取 YAML 文件，文件不存在返回空 dict。"""
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def _merge(yaml_data: dict) -> dict:
    """将 YAML 数据合并到 Python 默认值之上。"""
    paths = yaml_data.get("paths", {})
    project = yaml_data.get("project", {})
    charts = yaml_data.get("charts", {})

    return {
        "paths": {
            "raw_data": Path(paths.get("raw_data", str(_defaults.RAW_DATA_PATH))),
            "processed_dir": Path(paths.get("processed_dir", str(_defaults.PROCESSED_DATA_DIR))),
            "processed_data": Path(paths.get("processed_data", str(_defaults.PROCESSED_DATA_PATH))),
            "charts_dir": Path(paths.get("charts_dir", str(_defaults.CHARTS_OUTPUT_DIR))),
            "reports_dir": Path(paths.get("reports_dir", str(_defaults.REPORTS_OUTPUT_DIR))),
            "report_output": Path(paths.get("report_output", str(_defaults.REPORT_OUTPUT_PATH))),
        },
        "project": {
            "name": project.get("name", _defaults.PROJECT_NAME),
            "version": project.get("version", _defaults.VERSION),
        },
        "charts": {
            "figure_size": tuple(charts.get("figure_size", _defaults.CHART_FIGURE_SIZE)),
            "dpi": charts.get("dpi", _defaults.CHART_DPI),
            "font_family": charts.get("font_family", "Microsoft YaHei"),
        },
    }
