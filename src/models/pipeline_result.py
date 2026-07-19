"""PipelineResult — Pipeline 完整执行结果。"""
from dataclasses import dataclass, field
from pathlib import Path

from .customer_result import CustomerResult
from .sales_result import SalesResult


@dataclass
class PipelineResult:
    """Pipeline 完整执行结果，聚合所有阶段输出。"""

    sales_result: SalesResult
    customer_result: CustomerResult
    report_path: Path
    charts: list[str] = field(default_factory=list)
