"""CustomerResult — 客户分析结果。"""
from dataclasses import dataclass

import pandas as pd


@dataclass
class CustomerResult:
    """RFM 客户分层和地理分布结果。"""

    rfm_table: pd.DataFrame
    segment_stats: dict
    customers_by_country: pd.DataFrame
    top_customers: pd.DataFrame
    total_customers: int

    @classmethod
    def from_dict(cls, data: dict) -> "CustomerResult":
        """从 analyze_customers() 返回的 dict 构造实例。"""
        return cls(
            rfm_table=data["rfm_table"],
            segment_stats=data["segment_stats"],
            customers_by_country=data["customers_by_country"],
            top_customers=data["top_customers"],
            total_customers=data["total_customers"],
        )
