"""
模块：src.exceptions
职责：统一异常体系 — Pipeline 各阶段的类型化异常。

用法：
    from src.exceptions import ProjectError, DataLoadError
"""

from .exceptions import (
    AnalysisError,
    DataCleanError,
    DataLoadError,
    ProjectError,
    ReportGenerationError,
    VisualizationError,
)

__all__ = [
    "ProjectError",
    "DataLoadError",
    "DataCleanError",
    "AnalysisError",
    "VisualizationError",
    "ReportGenerationError",
]
