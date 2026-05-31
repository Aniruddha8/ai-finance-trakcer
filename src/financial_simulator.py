import pandas as pd
import numpy as np


class FinancialSimulator:
    """A modular simulator to project future account balances, savings metrics,

    and expense tracks based on historical user summaries.
    """

    def __init__(self, historical_summary_df: pd.DataFrame, user_id_col: str = "user_id"):
        self.history = historical_summary_df
        self.user_col = user_id_col

    def _extract_user_baseline(self, user_id: str) -> dict:
        """Extracts running baseline historical averages for a specific user."""
        user_data = self.history[self.history[self.user_col] == user_id]
        
        if user_data.empty:
            raise ValueError(f"User ID '{user_id}' not found in the historical summaries.")

        # Calculate base historical means for forecasting
        return {
            "avg_income": float(user_data["Total_Income"].mean()),
            "avg_expense": float(user_data["Total_Expense"].mean()),
            "avg_net_savings": float(user_data["Net_Savings"].mean())
        }

    def run_projection(
        self, 
        user_id: str, 
        months_to_project: int = 12, 
        starting_balance: float = 0.0,
        annual_income_growth_pct: float = 0.0,
        annual_expense_inflation_pct: float = 0.0,
        savings_optimization_pct: float = 0.0
    ) -> pd.DataFrame:
        """
        Generates a month-by-month financial projection.
        
        Parameters:
        - savings_optimization_pct: Shifts this % of income out of expenses directly into savings.
        """
        # 1. Fetch initial parameters from historical tracking data
        baseline = self._extract_user_baseline(user_id)
        
        income = baseline["avg_income"]
        expense = baseline["avg_expense"]
        
        # Apply immediate behavioral optimization if specified
        # (e.g., cutting expenses down to route more to savings instantly)
        optimization_shift = income * (savings_optimization_pct / 100.0)
        expense = max(0.0, expense - optimization_shift)

        # Convert annual percentage changes to compound monthly factors
        monthly_income_growth = (1 + (annual_income_growth_pct / 100.0)) ** (1/12) - 1
        monthly_expense_growth = (1 + (annual_expense_inflation_pct / 100.0)) ** (1/12) - 1

        # 2. Iteratively simulate months forward
        projection_records = []
        current_balance = starting_balance

        for month_idx in range(1, months_to_project + 1):
            # Step adjustments forward per compounding cycle
            if month_idx > 1:
                income *= (1 + monthly_income_growth)
                expense *= (1 + monthly_expense_growth)

            net_savings = income - expense
            current_balance += net_savings
            
            savings_rate = (net_savings / income * 100) if income > 0 else 0.0

            projection_records.append({
                "Month_Index": month_idx,
                "Projected_Income": round(income, 2),
                "Projected_Expense": round(expense, 2),
                "Net_Savings_Flow": round(net_savings, 2),
                "Cumulative_Account_Balance": round(current_balance, 2),
                "Projected_Savings_Rate_Pct": round(savings_rate, 2)
            })

        # 3. Compile output structure
        projection_df = pd.DataFrame(projection_records)
        return projection_df