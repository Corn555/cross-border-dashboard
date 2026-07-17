import sys

from src.data_loader import load_data
from src.data_profiler import profile_data
from src.data_cleaner import clean_data
from src.sales_analyzer import analyze_sales
from src.customer_analyzer import analyze_customers
from src.visualizer import create_charts


def main():
    """运行完整的数据分析流程。"""
    # 加载数据
    df = load_data("data/raw/sales.csv")
    if df is None:
        print("流程终止：数据加载失败。")
        return

    # Step 1: 数据质量诊断
    profile_data(df)

    # Step 2: 数据清洗
    result = clean_data(df)
    df_clean = result["dataframe"]

    # Step 3: 销售分析
    sales = analyze_sales(df_clean)

    # Step 4: 客户分析
    customers = analyze_customers(df_clean)

    # Step 5: 图表生成
    charts = create_charts(sales, customers)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
