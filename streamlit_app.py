import streamlit as st
from main import Executer

st.title("AI Finance Analyser")

uploaded_file=st.file_uploader("Chose CSV file",type=["csv"])

if uploaded_file is not None and st.button("Run Script"):
    r=Executer(uploaded_file,"category","transaction_type","user_1")
    response=r.execution()
    total_df=r.total_trend()
    monthly_df=r.monthly_trend()
    st.dataframe(total_df)

    #Convert the Period column to a plain string format ("YYYY-MM") as pandas direct value store causes issue.
    chart_data = monthly_df.copy()
    chart_data["month"] = chart_data["month"].astype(str)
    
    # Plot the converted dataframe
    st.bar_chart(chart_data, x="month", y=["Net_Savings", "Total_Expense"])

    with st.status("Analysing..", expanded=False, state="running", width="stretch") as status:
        st.write_stream(response)
        status.update(label="Analysis Complete", state="complete", expanded=False)
    st.button("Rerun")