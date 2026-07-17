"""
Module: sales_analyzer
Responsibility: Compute sales KPIs — revenue, trends, top products,
                top countries, average order value.
"""
import pandas as pd


def analyze_sales(df: pd.DataFrame) -> dict:
    """
    Compute all sales KPIs from the cleaned DataFrame.

    Args:
        df: Cleaned DataFrame (must have TotalSales, InvoiceDate,
            Description, Country, Invoice columns).

    Returns:
        dict with keys: total_revenue, total_orders, avg_order_value,
        total_customers, monthly_revenue (DataFrame),
        top_products (DataFrame), top_countries (DataFrame).
    """
    total_revenue = float(df["TotalSales"].sum())
    total_orders = int(df["Invoice"].nunique())
    total_customers = int(df["Customer ID"].nunique())
    avg_order_value = total_revenue / total_orders if total_orders else 0.0

    # Monthly revenue trend
    monthly_revenue = (
        df.set_index("InvoiceDate")
        .resample("ME")["TotalSales"]
        .sum()
        .reset_index()
    )
    monthly_revenue.columns = ["Month", "Revenue"]

    # Top 10 products by revenue
    top_products = (
        df.groupby("Description")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_products.columns = ["Product", "Revenue"]

    # Top 10 countries by revenue
    top_countries = (
        df.groupby("Country")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_countries.columns = ["Country", "Revenue"]

    # Top 10 countries by order count
    top_countries_orders = (
        df.groupby("Country")["Invoice"]
        .nunique()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_countries_orders.columns = ["Country", "Orders"]

    result = {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "avg_order_value": avg_order_value,
        "monthly_revenue": monthly_revenue,
        "top_products": top_products,
        "top_countries": top_countries,
        "top_countries_orders": top_countries_orders,
    }

    # --- Print summary ---
    print("\n" + "=" * 56)
    print("  SALES ANALYSIS")
    print("=" * 56)
    print(f"  Total Revenue       : $ {total_revenue:>12,.2f}")
    print(f"  Total Orders        :   {total_orders:>12,}")
    print(f"  Total Customers     :   {total_customers:>12,}")
    print(f"  Avg Order Value     : $ {avg_order_value:>12,.2f}")
    print("-" * 56)
    print("  Top 5 Products by Revenue")
    for _, row in top_products.head(5).iterrows():
        desc = str(row["Product"])[:38]
        print(f"  {desc:<38s} $ {row['Revenue']:>10,.0f}")
    print("-" * 56)
    print("  Top 5 Countries by Revenue")
    for _, row in top_countries.head(5).iterrows():
        print(f"  {row['Country']:<38s} $ {row['Revenue']:>10,.0f}")
    print("=" * 56 + "\n")

    return result
