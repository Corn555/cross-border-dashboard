"""SalesResult — 销售分析结果。"""
from dataclasses import dataclass

import pandas as pd


@dataclass
class SalesResult:
    """销售 KPI 和聚合分析结果。"""

    total_revenue: float
    total_orders: int
    total_customers: int
    avg_order_value: float
    monthly_revenue: pd.DataFrame
    top_products: pd.DataFrame
    top_countries: pd.DataFrame
    top_countries_orders: pd.DataFrame

    @classmethod
    def from_dict(cls, data: dict) -> "SalesResult":
        """从 analyze_sales() 返回的 dict 构造实例。"""
        return cls(
            total_revenue=data["total_revenue"],
            total_orders=data["total_orders"],
            total_customers=data["total_customers"],
            avg_order_value=data["avg_order_value"],
            monthly_revenue=data["monthly_revenue"],
            top_products=data["top_products"],
            top_countries=data["top_countries"],
            top_countries_orders=data["top_countries_orders"],
        )
