import pandas as pd
import streamlit as st #type: ignore

st.title("Salary Analyzer")

upload_file = st.file_uploader("Choose your CSV file", type=['csv'])

if upload_file is not None:
    dataframe = pd.read_csv(upload_file)
    
    st.write("### Data Preview")
    st.write(dataframe)
    
    # Find salary column (common names)
    salary_cols = [col for col in dataframe.columns if 'salary' in col.lower()]
    
    if salary_cols:
        salary_col = salary_cols[0]
        
        st.write("### Salary Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_salary = dataframe[salary_col].mean()
            st.metric("Average Salary", f"${avg_salary:,.2f}")
        
        with col2:
            max_salary = dataframe[salary_col].max()
            st.metric("Highest Salary", f"${max_salary:,.2f}")
        
        with col3:
            min_salary = dataframe[salary_col].min()
            st.metric("Lowest Salary", f"${min_salary:,.2f}")
    else:
        st.warning("No salary column found in the CSV file.")