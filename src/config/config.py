"""
模块：全局配置
职责：集中管理所有可配置参数，作为项目的单一配置来源。

用法：
    from src.config import RAW_DATA_PATH, VERSION
"""
from pathlib import Path

# ── 项目信息 ──────────────────────────────────
# 项目显示名称，用于终端输出和报告标题
PROJECT_NAME = "跨境电商销售数据分析平台"
# 当前版本号，遵循语义化版本规范
VERSION = "2.3.0"

# ── 数据路径 ──────────────────────────────────
# 原始 CSV 数据文件路径（只读，不修改）
RAW_DATA_PATH = Path("data/raw/sales.csv")
# 清洗后数据保存目录
PROCESSED_DATA_DIR = Path("data/processed")
# 清洗后数据文件完整路径
PROCESSED_DATA_PATH = Path("data/processed/sales_clean.csv")

# ── 输出路径 ──────────────────────────────────
# 图表 PNG 文件输出目录
CHARTS_OUTPUT_DIR = Path("output/charts")
# HTML 报告输出目录
REPORTS_OUTPUT_DIR = Path("output/reports")
# HTML 报告文件完整路径
REPORT_OUTPUT_PATH = Path("output/reports/report.html")

# ── 图表默认参数 ───────────────────────────────
# 默认图表尺寸 (宽度, 高度)，单位英寸
CHART_FIGURE_SIZE = (12, 6)
# 默认图表输出分辨率 DPI
CHART_DPI = 120
