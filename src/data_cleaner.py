"""
Module: data_cleaner
Responsibility: Clean raw data — remove invalid rows, fix types,
                add computed columns, save cleaned CSV.
"""
import pandas as pd


def clean_data(df: pd.DataFrame, output_path: str = "data/processed/sales_clean.csv") -> dict:
    """
    Clean the raw DataFrame and save the result to CSV.

    Steps:
    1. Drop fully duplicate rows
    2. Drop rows with null Customer ID
    3. Remove negative Quantity (returns/refunds)
    4. Remove zero Quantity and zero Price rows
    5. Convert InvoiceDate to datetime
    6. Create TotalSales = Quantity * Price

    Args:
        df: Raw DataFrame from the data loader.
        output_path: Where to save the cleaned CSV.

    Returns:
        dict with cleaned DataFrame and cleaning statistics.
    """
    rows_before = len(df)
    stats = {"rows_before": rows_before}

    # --- Step 1: Drop duplicates ---
    df = df.drop_duplicates()
    dupes_removed = rows_before - len(df)
    stats["duplicates_removed"] = dupes_removed

    # --- Step 2: Drop null Customer ID ---
    before = len(df)
    df = df.dropna(subset=["Customer ID"])
    stats["null_customer_removed"] = before - len(df)

    # --- Step 3: Remove negative Quantity ---
    before = len(df)
    df = df[df["Quantity"] > 0]
    stats["negative_qty_removed"] = before - len(df)

    # --- Step 4: Remove zero Quantity & zero Price ---
    before = len(df)
    df = df[(df["Quantity"] != 0) & (df["Price"] > 0)]
    stats["zero_removed"] = before - len(df)

    # --- Step 5: Convert types ---
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="%m/%d/%y %H:%M")
    df["Customer ID"] = df["Customer ID"].astype(int)

    # --- Step 6: Add computed column ---
    df["TotalSales"] = df["Quantity"] * df["Price"]

    rows_after = len(df)
    stats["rows_after"] = rows_after
    stats["total_removed"] = rows_before - rows_after

    # --- Save ---
    df.to_csv(output_path, index=False)
    stats["output_path"] = output_path

    # --- Print cleaning report ---
    print("\n" + "=" * 56)
    print("  DATA CLEANING REPORT")
    print("=" * 56)
    print(f"  Rows before cleaning : {rows_before:>10,}")
    print(f"  Rows after cleaning  : {rows_after:>10,}")
    print(f"  Total removed        : {rows_before - rows_after:>10,}  "
          f"({(rows_before - rows_after) / rows_before * 100:.1f}%)")
    print("-" * 56)
    print(f"  Duplicates           : {dupes_removed:>10,}")
    print(f"  Null Customer ID     : {stats['null_customer_removed']:>10,}")
    print(f"  Negative Quantity    : {stats['negative_qty_removed']:>10,}")
    print(f"  Zero Qty / Price     : {stats['zero_removed']:>10,}")
    print("-" * 56)
    print(f"  Cleaned data saved to: {output_path}")
    print("=" * 56 + "\n")

    return {"dataframe": df, "stats": stats}
