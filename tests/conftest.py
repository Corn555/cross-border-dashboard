"""
共享 test fixtures。
"""
import pandas as pd
import pytest


@pytest.fixture
def sample_raw_df() -> pd.DataFrame:
    """包含典型脏数据的迷你 DataFrame（模拟原始 CSV）。"""
    data = {
        "Invoice": ["INV001", "INV001", "INV002", "INV003", "INV004"],
        "StockCode": ["A", "A", "B", "C", "D"],
        "Description": ["Item A", "Item A", "Item B", "Item C", "Item D"],
        "Quantity": [2, 2, -1, 3, 0],
        "InvoiceDate": ["01/15/25 10:30", "01/15/25 10:30",
                        "02/20/25 14:00", "03/10/25 09:00", "04/01/25 12:00"],
        "Price": [10.0, 10.0, 20.0, 15.0, 5.0],
        "Customer ID": [1.0, 1.0, 2.0, None, 3.0],
        "Country": ["UK", "UK", "Germany", "UK", "France"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_clean_df() -> pd.DataFrame:
    """迷你清洗后数据集（已去重、无空值、有 TotalSales）。"""
    data = {
        "Invoice": ["INV001", "INV002", "INV003"],
        "Customer ID": [1, 2, 1],
        "Description": ["Item A", "Item B", "Item C"],
        "Quantity": [2, 1, 5],
        "Price": [10.0, 20.0, 15.0],
        "TotalSales": [20.0, 20.0, 75.0],
        "InvoiceDate": pd.to_datetime(["2025-01-15", "2025-02-20", "2025-03-10"]),
        "Country": ["UK", "Germany", "UK"],
    }
    return pd.DataFrame(data)
