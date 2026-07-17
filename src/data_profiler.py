"""
模块：数据诊断器
职责：诊断数据质量——只发现问题，不修改数据。
"""
import pandas as pd


def profile_data(df: pd.DataFrame) -> dict:
    """
    对原始数据执行全面的数据质量诊断，并打印报告。

    检查项：行列数、缺失值、重复行、负数量、空客户ID、零价格等异常。

    Args:
        df: 从 data_loader 加载的原始 DataFrame。

    Returns:
        dict，包含：row_count, col_count, dtypes, missing_pct,
        duplicate_count, negative_qty_count, null_customer_count,
        zero_price_count, total_memory_mb 等诊断指标。
    """
    total_rows = len(df)

    # --- 计算各项指标 ---
    missing_pct = (df.isnull().sum() / total_rows * 100).round(2)
    duplicate_count = int(df.duplicated().sum())
    negative_qty_count = int((df["Quantity"] < 0).sum())
    null_customer_count = int(df["Customer ID"].isnull().sum())
    zero_price_count = int((df["Price"] == 0).sum())
    zero_qty_count = int((df["Quantity"] == 0).sum())

    result = {
        "row_count": total_rows,
        "col_count": len(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "missing_pct": missing_pct.to_dict(),
        "duplicate_count": duplicate_count,
        "duplicate_pct": round(duplicate_count / total_rows * 100, 2),
        "negative_qty_count": negative_qty_count,
        "negative_qty_pct": round(negative_qty_count / total_rows * 100, 2),
        "null_customer_count": null_customer_count,
        "null_customer_pct": round(null_customer_count / total_rows * 100, 2),
        "zero_price_count": zero_price_count,
        "zero_qty_count": zero_qty_count,
        "total_memory_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
    }

    # --- 打印诊断报告 ---
    print("\n" + "=" * 56)
    print("  数据质量诊断报告")
    print("=" * 56)
    print(f"  总行数             : {total_rows:>12,}")
    print(f"  总列数             : {len(df.columns):>12}")
    print(f"  内存占用           : {result['total_memory_mb']:>10.2f} MB")
    print(f"  重复行             : {duplicate_count:>12,}  ({result['duplicate_pct']}%)")
    print("-" * 56)
    print("  异常检测")
    print(f"  负数量（退货）     : {negative_qty_count:>12,}  ({result['negative_qty_pct']}%)")
    print(f"  零数量             : {zero_qty_count:>12,}")
    print(f"  零价格             : {zero_price_count:>12,}")
    print(f"  空客户ID           : {null_customer_count:>12,}  ({result['null_customer_pct']}%)")
    print("-" * 56)
    print("  缺失值比例 (%)")
    missing_found = False
    for col, pct in missing_pct.items():
        if pct > 0:
            print(f"  {col:<20s}: {pct:>8.2f}%")
            missing_found = True
    if not missing_found:
        print("  未发现缺失值。")
    print("-" * 56)
    print("  字段数据类型")
    for col, dtype in result["dtypes"].items():
        print(f"  {col:<20s}: {str(dtype):>12}")
    print("=" * 56 + "\n")

    return result
