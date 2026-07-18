"""Tests for src.data_cleaner."""
import pandas as pd

from src.data_cleaner import clean_data


def test_clean_removes_duplicates(sample_raw_df, tmp_path):
    """应移除完全重复的行。"""
    out = tmp_path / "clean.csv"
    result = clean_data(sample_raw_df, output_path=str(out))
    stats = result["stats"]
    assert stats["duplicates_removed"] == 1  # INV001 重复一次


def test_clean_removes_null_customer(sample_raw_df, tmp_path):
    """应移除 Customer ID 为空的行。"""
    out = tmp_path / "clean.csv"
    result = clean_data(sample_raw_df, output_path=str(out))
    stats = result["stats"]
    assert stats["null_customer_removed"] == 1


def test_clean_removes_negative_qty(sample_raw_df, tmp_path):
    """应移除负数量行（退货）。"""
    out = tmp_path / "clean.csv"
    result = clean_data(sample_raw_df, output_path=str(out))
    stats = result["stats"]
    assert stats["negative_qty_removed"] >= 1  # INV002 qty=-1


def test_clean_adds_totalsales(sample_raw_df, tmp_path):
    """清洗后应包含 TotalSales = Quantity * Price 列。"""
    out = tmp_path / "clean.csv"
    result = clean_data(sample_raw_df, output_path=str(out))
    df_clean = result["dataframe"]
    assert "TotalSales" in df_clean.columns
    assert (df_clean["TotalSales"] == df_clean["Quantity"] * df_clean["Price"]).all()


def test_clean_output_file(sample_raw_df, tmp_path):
    """清洗后应生成 CSV 文件。"""
    out = tmp_path / "clean.csv"
    clean_data(sample_raw_df, output_path=str(out))
    assert out.exists()
    saved = pd.read_csv(out)
    assert len(saved) > 0
