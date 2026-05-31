import pandas as pd


class TrendAnalyser:
    """A modular class to calculate user-level financial KPIs using pre-existing
    'transaction_type' classifications and dynamic category tracking (excluding income).
    """

    def __init__(
        self,
        user_id,
        amount_col: str = "amount",
        user_col: str = "user_id",
        date_col: str = "date",
        type_col: str = "transaction_type",
        category_col: str = "category",
    ):
        self.amount_col = amount_col
        self.user_col = user_col
        self.date_col = date_col
        self.type_col = type_col
        self.category_col = category_col
        self.user_id=user_id
        
        # Define categories to exclude from spend metrics
        self.income_categories = ["Salary", "Bonus", "Interest"]

    def _prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Helper to validate schema and extract clean cashflows based on explicit text types."""
        required_cols = [
            self.amount_col,
            self.user_col,
            self.date_col,
            self.type_col,
            self.category_col,
        ]
        for col in required_cols:
            if col not in df.columns:
                raise KeyError(
                    f"Required column '{col}' is missing from the DataFrame."
                )

        working_df = df[df["user_id"]==self.user_id].copy()

        # Extract values strictly based on your pre-existing 'transaction_type' strings
        working_df["Income"] = (
            working_df[self.amount_col]
            .where(working_df[self.type_col] == "Income", 0.0)
            .abs()
        )
        working_df["Expense"] = (
            working_df[self.amount_col]
            .where(working_df[self.type_col] == "Expense", 0.0)
            .abs()
        )

        # Net balance calculation: Income (Inflow) minus Expense (Outflow)
        working_df["Net"] = working_df["Income"] - working_df["Expense"]

        return working_df

    def _get_category_aggregations(self, df: pd.DataFrame) -> dict:
        """Dynamically builds a dictionary of named aggregations for true spend categories."""
        unique_categories = df[self.category_col].dropna().unique()
        cat_aggs = {}

        for cat in unique_categories:
            # Skip income-related categories so they aren't tracked as spend
            if cat in self.income_categories:
                continue
                
            # Create a temporary column containing only that category's absolute amount, else 0
            df[f"cat_{cat}"] = (
                df[self.amount_col].where(df[self.category_col] == cat, 0.0).abs()
            )
            # Define the aggregation tuple: (temporary_column, aggregation_function)
            cat_aggs[f"Spend_{cat}"] = (f"cat_{cat}", "sum")

        return cat_aggs

    def calculate_user_monthly_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Groups pre-classified data by user and month, appending true spend breakdowns."""
        working_df = self._prepare_data(df)
        working_df["month"] = working_df[self.date_col].dt.to_period("M")

        # Capture dynamic category aggregations (ignoring salary, bonus, interest)
        category_aggs = self._get_category_aggregations(working_df)

        # Base KPIs
        base_aggs = {
            "Total_Income": ("Income", "sum"),
            "Total_Expense": ("Expense", "sum"),
            "Net_Savings": ("Net", "sum"),
        }

        # Combine base KPIs with the filtered category spend metrics
        all_aggs = {**base_aggs, **category_aggs}

        grouped = working_df.groupby([self.user_col, "month"], as_index=False).agg(
            **all_aggs
        )

        # Calculate Savings Rate
        grouped["Savings_Rate_Pct"] = (
            (grouped["Net_Savings"] / grouped["Total_Income"]) * 100
        ).where(grouped["Total_Income"] > 0, 0.0).round(2)

        # Reorder columns
        cols = [
            self.user_col,
            "month",
            "Total_Income",
            "Total_Expense",
            "Net_Savings",
            "Savings_Rate_Pct",
        ] + list(category_aggs.keys())

        return (
            grouped[cols]
            .sort_values(by=[self.user_col, "month"])
            .reset_index(drop=True)
        )

    def calculate_user_total_savings(self, df: pd.DataFrame) -> pd.DataFrame:
        """Computes dataset-wide totals per user, appending lifetime spend breakdowns."""
        working_df = self._prepare_data(df)

        # Capture dynamic category aggregations (ignoring salary, bonus, interest)
        category_aggs = self._get_category_aggregations(working_df)

        # Base KPIs
        base_aggs = {
            "Lifetime_Income": ("Income", "sum"),
            "Lifetime_Expense": ("Expense", "sum"),
            "Cumulative_Savings": ("Net", "sum"),
        }

        all_aggs = {**base_aggs, **category_aggs}

        total_grouped = working_df.groupby(self.user_col, as_index=False).agg(
            **all_aggs
        )

        # Calculate Lifetime Savings Rate
        total_grouped["Lifetime_Savings_Rate_Pct"] = (
            (total_grouped["Cumulative_Savings"] / total_grouped["Lifetime_Income"])
            * 100
        ).where(total_grouped["Lifetime_Income"] > 0, 0.0).round(2)

        # Reorder columns
        cols = [
            self.user_col,
            "Lifetime_Income",
            "Lifetime_Expense",
            "Cumulative_Savings",
            "Lifetime_Savings_Rate_Pct",
        ] + list(category_aggs.keys())

        return total_grouped[cols].reset_index(drop=True)