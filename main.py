# main.py
from src.data_loader import TransactionLoader
from src.transaction_classifier import TransactionClassifier
from src.trend_analysis import TrendAnalyser
from src.llm_call import AIBanker

class Executer:
    def __init__(self,path,source_col,target_col,user_id):
        self.path=path
        self.source_col=source_col
        self.target_col=target_col
        self.user_id=user_id
        # Add a placeholder to cache the dataframe once loaded/classified
        self._classified_df = None

    def classifier(self):
        if self._classified_df is None:
            loader = TransactionLoader(self.path)
            df=loader.load_data()
            classifier = TransactionClassifier()
            self._classified_df = classifier.classify(df, source_col=self.source_col, target_col=self.target_col)
        return self._classified_df
    
    def total_trend(self):
        classified_df=self.classifier()
        aggregator = TrendAnalyser(self.user_id)
        user_report_total=aggregator.calculate_user_total_savings(classified_df)
        return user_report_total
    
    def monthly_trend(self):
        classified_df=self.classifier()
        aggregator = TrendAnalyser(self.user_id)
        user_report_monthly = aggregator.calculate_user_monthly_summary(classified_df)
        return user_report_monthly
    
    def execution(self):
        user_report_monthly=self.monthly_trend()
        user_report_total=self.total_trend()
        
        ai_object=AIBanker()
        ai_response=ai_object.FinancialAdvise(user_report_monthly,user_report_total,self.user_id)
        return ai_response
    
"""r=Executer(r"ai-finance-tracker\Data\customer_data.csv","category","transaction_type","user_1")
total_df=r.total_trend()
print(total_df)"""