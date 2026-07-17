from src.data_loader import load_data
from src.data_profiler import profile_data
from src.data_cleaner import clean_data


def main():
    """Run the full data analysis pipeline."""
    # Load
    df = load_data("data/raw/sales.csv")
    if df is None:
        print("Pipeline stopped: failed to load data.")
        return

    # Step 1: Diagnose data quality
    profile_data(df)

    # Step 2: Clean data
    result = clean_data(df)
    df_clean = result["dataframe"]


if __name__ == "__main__":
    main()
