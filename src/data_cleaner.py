"""
模块：数据清洗器
职责：清洗原始数据——去重、去空、去异常、修正类型、添加计算列、保存清洗后的CSV。
"""
import pandas as pd


def clean_data(df: pd.DataFrame, output_path: str = "data/processed/sales_clean.csv") -> dict:
    """
    清洗原始 DataFrame 并将结果保存为 CSV。

    清洗步骤：
    1. 删除完全重复的行
    2. 删除 Customer ID 为空的行
    3. 删除负数量（退货/退款记录）
    4. 删除零数量和零价格行
    5. InvoiceDate 转为 datetime，Customer ID 转为 int
    6. 添加计算列 TotalSales = Quantity * Price

    Args:
        df: 从 data_loader 加载的原始 DataFrame。
        output_path: 清洗后 CSV 的保存路径。

    Returns:
        dict，包含 cleaned DataFrame 和清洗统计信息。
    """
    rows_before = len(df)
    stats = {"rows_before": rows_before}

    # --- 第1步：去重 ---
    df = df.drop_duplicates()
    dupes_removed = rows_before - len(df)
    stats["duplicates_removed"] = dupes_removed

    # --- 第2步：删除空 Customer ID ---
    before = len(df)
    df = df.dropna(subset=["Customer ID"])
    stats["null_customer_removed"] = before - len(df)

    # --- 第3步：删除负数量（退货） ---
    before = len(df)
    df = df[df["Quantity"] > 0]
    stats["negative_qty_removed"] = before - len(df)

    # --- 第4步：删除零数量和零价格 ---
    before = len(df)
    df = df[(df["Quantity"] != 0) & (df["Price"] > 0)]
    stats["zero_removed"] = before - len(df)

    # --- 第5步：类型转换 ---
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="%m/%d/%y %H:%M")
    df["Customer ID"] = df["Customer ID"].astype(int)

    # --- 第6步：添加计算列 ---
    df["TotalSales"] = df["Quantity"] * df["Price"]

    rows_after = len(df)
    stats["rows_after"] = rows_after
    stats["total_removed"] = rows_before - rows_after

    # --- 保存 ---
    df.to_csv(output_path, index=False)
    stats["output_path"] = output_path

    # --- 打印清洗报告 ---
    print("\n" + "=" * 56)
    print("  数据清洗报告")
    print("=" * 56)
    print(f"  清洗前行数         : {rows_before:>10,}")
    print(f"  清洗后行数         : {rows_after:>10,}")
    print(f"  共移除             : {rows_before - rows_after:>10,}  "
          f"({(rows_before - rows_after) / rows_before * 100:.1f}%)")
    print("-" * 56)
    print(f"  重复行             : {dupes_removed:>10,}")
    print(f"  空客户ID           : {stats['null_customer_removed']:>10,}")
    print(f"  负数量（退货）     : {stats['negative_qty_removed']:>10,}")
    print(f"  零数量/零价格      : {stats['zero_removed']:>10,}")
    print("-" * 56)
    print(f"  清洗后数据已保存至: {output_path}")
    print("=" * 56 + "\n")

    return {"dataframe": df, "stats": stats}
