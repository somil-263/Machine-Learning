import pandas as pd
import streamlit as st #type: ignore

st.title("Chart Designer")
data = st.file_uploader("Choose the csv file", type=['csv'])

if data is not None:
    dataframe = pd.read_csv(data)
    st.write("### Uploaded data")
    st.write(dataframe)

    numeric_cols = dataframe.select_dtypes(include=['number']).columns.tolist()
    chart_type = st.selectbox("Choose chart type", ["Line", "Bar", "Area", "Histogram"])

    if chart_type == "Histogram":
        if numeric_cols:
            hist_col = st.selectbox("Choose numeric column", numeric_cols)
            if hist_col:
                st.write(f"### Histogram for {hist_col}")
                st.bar_chart(dataframe[hist_col].value_counts().sort_index())
        else:
            st.warning("No numeric columns available for histogram.")
    else:
        x_axis = st.selectbox("Choose x-axis", dataframe.columns.tolist())
        y_axis = st.selectbox("Choose y-axis", numeric_cols if numeric_cols else dataframe.columns.tolist())
        if x_axis and y_axis:
            plot_data = dataframe.set_index(x_axis)[y_axis]
            st.write(f"### {chart_type} chart")
            if chart_type == "Line":
                st.line_chart(plot_data)
            elif chart_type == "Bar":
                st.bar_chart(plot_data)
            elif chart_type == "Area":
                st.area_chart(plot_data)

