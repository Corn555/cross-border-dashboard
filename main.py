from src.data_loader import load_data


def main():
    df = load_data("data/raw/sales.csv")

    if df is not None:
        print(df.head())
        print(df.shape)
        print(df.columns)
        print(df.info())
        print(df.describe())





if __name__ == "__main__":
    main()


