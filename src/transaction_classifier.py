import pandas as pd
from typing import List, Dict


class TransactionClassifier:
    """A modular class to handle business logic classification on a transaction DataFrame."""

    def __init__(self,custom_mapping: Dict[str, List[str]] = None):
        # Default taxonomy as specified by the rules
        if custom_mapping is None:
            self.rules = {
                "Expense": [
                    "Groceries", "Rent", "Utilities", "Entertainment",
                    "Dining", "Transport", "Healthcare", "Education", 
                    "Savings Transfer"
                ],
                "Income": [
                    "Salary", "Bonus", "Interest"
                ]
            }
        else:
            self.rules = custom_mapping
            
        # Invert the rules dictionary to a fast O(1) lookup format: {item: category_type}
        self.mapping_index = self._build_lookup_index()

    def _build_lookup_index(self) -> Dict[str, str]:
        """Flattens the category rules array into a key-value hash map."""
        lookup = {}
        for classification, categories in self.rules.items():
            for cat in categories:
                lookup[cat] = classification
        return lookup

    def classify(self, df: pd.DataFrame, source_col: str = "category", target_col: str = "transaction_type") -> pd.DataFrame:
        """
        Categorizes an existing DataFrame in place or returned safely.
        
        Parameters:
        df (pd.DataFrame): The input DataFrame.
        source_col (str): The column with fine-grained tags (e.g., 'Groceries').
        target_col (str): The new column to write classifications to (e.g., 'Expense').
        """
        if source_col not in df.columns:
            raise KeyError(f"The source column '{source_col}' does not exist in the provided DataFrame.")

        # Create a clean copy to prevent SettingWithCopyWarning if working on slices
        processed_df = df.copy()

        # .map() maps keys to values, and .fillna('Other') catches everything else safely
        processed_df[target_col] = (
            processed_df[source_col]
            .map(self.mapping_index)
            .fillna("Other")
        )
        
        return processed_df