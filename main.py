from src.data_loader import load_data
from src.data_profiler import profile_data


def main():
    """Run the full data analysis pipeline."""
    df = load_data("data/raw/sales.csv")

    if df is None:
        print("Pipeline stopped: failed to load data.")
        return

    # Step 1: Diagnose data quality
    profile_data(df)


if __name__ == "__main__":
    main()
