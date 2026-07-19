"""
模块：src.models
职责：项目数据模型定义。

用法：
    from src.models import PipelineResult, SalesResult, CustomerResult
"""

from .customer_result import CustomerResult
from .pipeline_result import PipelineResult
from .sales_result import SalesResult

__all__ = ["PipelineResult", "SalesResult", "CustomerResult"]
