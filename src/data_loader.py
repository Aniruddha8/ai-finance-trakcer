import pandas as pd
import numpy as np


class TransactionLoader:
    """A modular class to load and perform basic EDA on transaction data."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

        # Define expected columns and their expected types for safety
        self.expected_columns = [
            "transaction_id",
            "user_id",
            "date",
            "category",
            "amount",
            "payment_method",
            "merchant",
            "description",
        ]

    def load_data(self) -> pd.DataFrame:
        """Loads the CSV file, validates columns, and parses dates."""
        try:
            # Parse dates on load to save a step later
            self.df = pd.read_csv(self.file_path, parse_dates=["date"])
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file at {self.file_path} was not found.")
        except Exception as e:
            raise Exception(f"An error occurred while reading the file: {e}")

        # Validate that all required columns exist
        missing_cols = [col for col in self.expected_columns if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"CSV missing mandatory columns: {missing_cols}")

        print(
            f"Successfully loaded {self.df.shape[0]} rows and {self.df.shape[1]} columns."
        )
        return self.df

    def get_basic_info(self) -> dict:
        """Returns structural info, missing values, and data types."""
        if self.df is None:
            raise ValueError("Data not loaded. Run load_data() first.")

        info = {
            "shape": self.df.shape,
            "missing_values": self.df.isnull().sum().to_dict(),
            "data_types": self.df.dtypes.to_dict(),
            "duplicate_transactions": int(self.df.duplicated(subset=["transaction_id"]).sum()),
        }
        return info

    def get_numerical_summary(self) -> pd.DataFrame:
        """Returns statistical summary of the 'amount' column."""
        if self.df is None:
            raise ValueError("Data not loaded. Run load_data() first.")

        # Generates count, mean, std, min, 25%, 50%, 75%, max
        return self.df[["amount"]].describe()

    def get_categorical_breakdown(self) -> dict:
        """Returns value counts and unique counts for key categorical columns."""
        if self.df is None:
            raise ValueError("Data not loaded. Run load_data() first.")

        categorical_cols = ["category", "payment_method", "merchant"]
        breakdown = {}

        for col in categorical_cols:
            breakdown[col] = {
                "unique_count": self.df[col].nunique(),
                "top_values": self.df[col].value_counts().to_dict(),
            }

        return breakdown

    def get_time_bounds(self) -> dict:
        """Returns the start date, end date, and overall span of the dataset."""
        if self.df is None:
            raise ValueError("Data not loaded. Run load_data() first.")

        if not pd.api.types.is_datetime64_any_dtype(self.df["date"]):
            raise TypeError("The 'date' column must be converted to datetime first.")

        min_date = self.df["date"].min()
        max_date = self.df["date"].max()

        return {
            "start_date": min_date,
            "end_date": max_date,
            "days_span": (max_date - min_date).days,
        }

    def run_full_eda(self):
        """Prints a comprehensive text-based EDA report to the console."""
        self.load_data()

        print("\n" + "=" * 40)
        print("      TRANSACTION DATA EDA REPORT       ")
        print("=" * 40)

        # 1. Structure
        info = self.get_basic_info()
        print(f"\n[1] Dataset Shape: {info['shape'][0]} rows, {info['shape'][1]} columns")
        print(f"    Duplicate transaction_ids: {info['duplicate_transactions']}")

        # 2. Missing Data
        print("\n[2] Missing Values per Column:")
        for col, count in info["missing_values"].items():
            print(f"    - {col}: {count}")

        # 3. Time Frame
        time_info = self.get_time_bounds()
        print(f"\n[3] Date Range Covered:")
        print(f"    - From: {time_info['start_date'].strftime('%Y-%m-%d')}")
        print(f"    - To:   {time_info['end_date'].strftime('%Y-%m-%d')}")
        print(f"    - Span: {time_info['days_span']} days")

        # 4. Financial Metrics
        print("\n[4] Financial Amount Summary:")
        print(self.get_numerical_summary())

        # 5. Categories & Sourcing
        print("\n[5] Categorical Breakdowns")
        cat_info = self.get_categorical_breakdown()
        for col, data in cat_info.items():
            print(f"    * Column: {col} ({data['unique_count']} unique values)")
            for val, count in data["top_values"].items():
                print(f"      - {val}: {count}")
    
