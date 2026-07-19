"""
模块：Pipeline
职责：编排完整的数据分析流程 — 加载 → 诊断 → 清洗 → 分析 → 图表 → 报告。

属于 Application Layer（Service Layer），不包含业务计算逻辑。
所有业务逻辑委托给 src/ 分析模块。
"""
from pathlib import Path

from src.customer_analyzer import analyze_customers
from src.data_cleaner import clean_data
from src.data_loader import load_data
from src.data_profiler import profile_data
from src.exceptions import (
    AnalysisError,
    DataCleanError,
    DataLoadError,
    ReportGenerationError,
    VisualizationError,
)
from src.logger import get_logger
from src.models import CustomerResult, PipelineResult, SalesResult
from src.report_generator import generate_report
from src.sales_analyzer import analyze_sales
from src.visualizer import create_charts

logger = get_logger(__name__)


def run_pipeline(
    raw_data_path: str | Path,
    processed_data_path: str | Path,
    charts_output_dir: str | Path,
    report_output_path: str | Path,
) -> PipelineResult:
    """
    执行完整的数据分析流程。

    编排 6 个阶段：加载 → 诊断 → 清洗 → 分析 → 图表 → 报告。
    任何阶段失败均抛出对应的 ProjectError 子类。

    Args:
        raw_data_path: 原始 CSV 数据文件路径。
        processed_data_path: 清洗后数据保存路径。
        charts_output_dir: 图表输出目录。
        report_output_path: HTML 报告输出路径。

    Returns:
        PipelineResult: sales_result, customer_result, report_path, charts。

    Raises:
        DataLoadError: 数据文件无法读取。
        DataCleanError: 数据清洗过程异常。
        AnalysisError: 分析计算失败。
        VisualizationError: 图表生成失败。
        ReportGenerationError: 报告生成失败。
    """
    logger.info("Pipeline started")

    # 统一转为 str，保证对业务模块向后兼容
    raw_path = str(raw_data_path)
    processed_path = str(processed_data_path)
    charts_dir = str(charts_output_dir)
    report_path = Path(report_output_path)

    # ── 阶段 1: 数据加载 ──
    df = load_data(raw_path)
    if df is None:
        raise DataLoadError(f"数据文件加载失败: {raw_path}")
    logger.info("Data loaded: %d rows x %d columns", df.shape[0], df.shape[1])

    # ── 阶段 2: 数据质量诊断 ──
    try:
        profile_data(df)
    except Exception as e:
        raise AnalysisError("数据质量诊断失败") from e

    # ── 阶段 3: 数据清洗 ──
    try:
        result = clean_data(df, output_path=processed_path)
    except Exception as e:
        raise DataCleanError("数据清洗失败") from e
    df_clean = result["dataframe"]
    stats = result["stats"]
    logger.info("Data cleaned: %d -> %d rows (%.1f%% removed)",
                stats["rows_before"], stats["rows_after"],
                stats["total_removed"] / stats["rows_before"] * 100)

    # ── 阶段 4: 业务分析 ──
    try:
        sales = analyze_sales(df_clean)
        customers = analyze_customers(df_clean)
    except Exception as e:
        raise AnalysisError("数据分析失败") from e
    logger.info("Analysis completed: revenue $%.2f, customers %d",
                sales["total_revenue"], customers["total_customers"])

    # ── 阶段 5: 图表生成 ──
    try:
        charts = create_charts(sales, customers, output_dir=charts_dir)
    except Exception as e:
        raise VisualizationError("图表生成失败") from e

    # ── 阶段 6: 报告生成 ──
    try:
        generate_report(sales, customers, charts,
                        cleaning_stats=stats,
                        output_path=str(report_path))
    except Exception as e:
        raise ReportGenerationError("报告生成失败") from e
    logger.info("Report generated: %s", report_path)

    logger.info("Pipeline finished")
    return PipelineResult(
        sales_result=SalesResult.from_dict(sales),
        customer_result=CustomerResult.from_dict(customers),
        report_path=report_path,
        charts=charts,
    )
