"""向后兼容 re-export。新代码请直接从 src.models 导入。"""
from .customer_result import CustomerResult
from .pipeline_result import PipelineResult
from .sales_result import SalesResult

__all__ = ["PipelineResult", "SalesResult", "CustomerResult"]
