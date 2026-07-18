"""
模块：数据模型
职责：定义 Pipeline 各阶段的返回数据结构。
"""
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PipelineResult:
    """Pipeline 完整执行结果。"""

    sales_result: dict
    customer_result: dict
    report_path: Path
    charts: list[str] = field(default_factory=list)
