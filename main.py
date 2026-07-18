import sys

from src.config import (
    CHARTS_OUTPUT_DIR,
    PROCESSED_DATA_PATH,
    RAW_DATA_PATH,
    REPORT_OUTPUT_PATH,
    VERSION,
)
from src.data_loader import load_data
from src.data_profiler import profile_data
from src.data_cleaner import clean_data
from src.sales_analyzer import analyze_sales
from src.customer_analyzer import analyze_customers
from src.visualizer import create_charts
from src.report_generator import generate_report


def main():
    """运行完整的数据分析流程。"""
    print(f"  版本: {VERSION}")

    # 加载数据
    df = load_data(RAW_DATA_PATH)
    if df is None:
        print("流程终止：数据加载失败。")
        return

    # Step 1: 数据质量诊断
    profile_data(df)

    # Step 2: 数据清洗
    result = clean_data(df, output_path=PROCESSED_DATA_PATH)
    df_clean = result["dataframe"]

    # Step 3: 销售分析
    sales = analyze_sales(df_clean)

    # Step 4: 客户分析
    customers = analyze_customers(df_clean)

    # Step 5: 图表生成
    charts = create_charts(sales, customers, output_dir=CHARTS_OUTPUT_DIR)

    # Step 6: 生成 HTML 报告
    generate_report(sales, customers, charts,
                    cleaning_stats=result["stats"],
                    output_path=REPORT_OUTPUT_PATH)

    print("=" * 56)
    print("  全部分析流程完成！")
    print(f"  报告位置: {REPORT_OUTPUT_PATH}")
    print("=" * 56 + "\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
