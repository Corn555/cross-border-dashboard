import sys

from src.config import (
    CHARTS_OUTPUT_DIR,
    PROCESSED_DATA_PATH,
    RAW_DATA_PATH,
    REPORT_OUTPUT_PATH,
    VERSION,
)
from src.logger import setup_logging, get_logger
from src.data_loader import load_data
from src.data_profiler import profile_data
from src.data_cleaner import clean_data
from src.sales_analyzer import analyze_sales
from src.customer_analyzer import analyze_customers
from src.visualizer import create_charts
from src.report_generator import generate_report

logger = get_logger(__name__)


def main():
    """运行完整的数据分析流程。"""
    logger.info("Program started (v%s)", VERSION)

    # 加载数据
    df = load_data(RAW_DATA_PATH)
    if df is None:
        logger.error("流程终止：数据加载失败。")
        return
    logger.info("Data loaded: %d rows x %d columns", df.shape[0], df.shape[1])

    # Step 1: 数据质量诊断
    profile_data(df)

    # Step 2: 数据清洗
    result = clean_data(df, output_path=PROCESSED_DATA_PATH)
    df_clean = result["dataframe"]
    stats = result["stats"]
    logger.info("Data cleaned: %d -> %d rows (%.1f%% removed)",
                stats["rows_before"], stats["rows_after"],
                stats["total_removed"] / stats["rows_before"] * 100)

    # Step 3: 销售分析
    sales = analyze_sales(df_clean)

    # Step 4: 客户分析
    customers = analyze_customers(df_clean)
    logger.info("Analysis completed: revenue $%.2f, customers %d",
                sales["total_revenue"], customers["total_customers"])

    # Step 5: 图表生成
    charts = create_charts(sales, customers, output_dir=CHARTS_OUTPUT_DIR)

    # Step 6: 生成 HTML 报告
    generate_report(sales, customers, charts,
                    cleaning_stats=stats,
                    output_path=REPORT_OUTPUT_PATH)
    logger.info("Report generated: %s", REPORT_OUTPUT_PATH)

    print("=" * 56)
    print("  全部分析流程完成！")
    print(f"  报告位置: {REPORT_OUTPUT_PATH}")
    print("=" * 56 + "\n")
    logger.info("Program finished")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    setup_logging()
    main()
