"""Tests for src.data_loader."""
import pandas as pd

from src.data_loader import load_data


def test_load_valid_csv(tmp_path):
    """加载有效 CSV 文件应返回 DataFrame。"""
    csv_path = tmp_path / "test.csv"
    pd.DataFrame({"A": [1, 2], "B": [3, 4]}).to_csv(csv_path, index=False)

    result = load_data(str(csv_path))
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2, 2)


def test_load_missing_file():
    """加载不存在的文件应返回 None。"""
    result = load_data("nonexistent_file.csv")
    assert result is None


def test_load_csv_columns(tmp_path):
    """加载的 DataFrame 应包含预期的列。"""
    csv_path = tmp_path / "test.csv"
    pd.DataFrame({"X": [1], "Y": [2]}).to_csv(csv_path, index=False)

    result = load_data(str(csv_path))
    assert list(result.columns) == ["X", "Y"]
