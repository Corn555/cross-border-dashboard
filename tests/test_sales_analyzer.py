"""Tests for src.sales_analyzer."""
from src.sales_analyzer import analyze_sales


def test_total_revenue(sample_clean_df):
    """总营收应为所有行的 Quantity * Price 之和。"""
    result = analyze_sales(sample_clean_df)
    # 2*10 + 1*20 + 5*15 = 20 + 20 + 75 = 115
    assert result["total_revenue"] == 115.0


def test_total_orders(sample_clean_df):
    """总订单数应为唯一 Invoice 数量。"""
    result = analyze_sales(sample_clean_df)
    assert result["total_orders"] == 3


def test_total_customers(sample_clean_df):
    """总客户数应为唯一 Customer ID 数量。"""
    result = analyze_sales(sample_clean_df)
    assert result["total_customers"] == 2  # Customer 1 and 2


def test_avg_order_value(sample_clean_df):
    """平均客单价 = total_revenue / total_orders。"""
    result = analyze_sales(sample_clean_df)
    assert result["avg_order_value"] == 115.0 / 3


def test_top_products(sample_clean_df):
    """Top products 应按营收降序排列。"""
    result = analyze_sales(sample_clean_df)
    top = result["top_products"]
    assert len(top) > 0
    assert top.iloc[0]["Revenue"] >= top.iloc[-1]["Revenue"]


def test_top_countries(sample_clean_df):
    """Top countries 应包含 Germany 和 UK。"""
    result = analyze_sales(sample_clean_df)
    countries = set(result["top_countries"]["Country"])
    assert "UK" in countries
    assert "Germany" in countries


def test_monthly_revenue(sample_clean_df):
    """月度营收 DataFrame 应包含 Month 和 Revenue 列。"""
    result = analyze_sales(sample_clean_df)
    monthly = result["monthly_revenue"]
    assert "Month" in monthly.columns
    assert "Revenue" in monthly.columns
    assert len(monthly) >= 1
