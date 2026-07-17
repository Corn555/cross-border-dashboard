"""
Module: data_profiler
Responsibility: Diagnose data quality — detect problems, don't fix them.
"""
import pandas as pd


def profile_data(df: pd.DataFrame) -> dict:
    """
    Run a full data quality diagnosis and print a report.

    Checks: row/column count, missing values, duplicates, negative
    quantities, null Customer IDs, and basic statistical anomalies.

    Args:
        df: Raw DataFrame from the data loader.

    Returns:
        dict with keys: row_count, col_count, dtypes, missing_pct,
        duplicate_count, negative_qty_count, null_customer_count,
        zero_price_count, total_memory_mb.
    """
    total_rows = len(df)

    # --- Compute all metrics ---
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

    # --- Print report ---
    print("\n" + "=" * 56)
    print("  DATA QUALITY REPORT")
    print("=" * 56)
    print(f"  Rows              : {total_rows:>12,}")
    print(f"  Columns           : {len(df.columns):>12}")
    print(f"  Memory Usage      : {result['total_memory_mb']:>10.2f} MB")
    print(f"  Duplicate Rows    : {duplicate_count:>12,}  ({result['duplicate_pct']}%)")
    print("-" * 56)
    print("  ANOMALY DETECTION")
    print(f"  Negative Quantity : {negative_qty_count:>12,}  ({result['negative_qty_pct']}%)")
    print(f"  Zero Quantity     : {zero_qty_count:>12,}")
    print(f"  Zero Price        : {zero_price_count:>12,}")
    print(f"  Null Customer ID  : {null_customer_count:>12,}  ({result['null_customer_pct']}%)")
    print("-" * 56)
    print("  MISSING VALUES (%)")
    missing_found = False
    for col, pct in missing_pct.items():
        if pct > 0:
            print(f"  {col:<20s}: {pct:>8.2f}%")
            missing_found = True
    if not missing_found:
        print("  No missing values found.")
    print("-" * 56)
    print("  COLUMN DATA TYPES")
    for col, dtype in result["dtypes"].items():
        print(f"  {col:<20s}: {str(dtype):>12}")
    print("=" * 56 + "\n")

    return result
