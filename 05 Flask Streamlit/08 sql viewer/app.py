import streamlit as st
import sqlite3
import pandas as pd
import tempfile
import os

st.set_page_config(page_title="SQLite Web Viewer", page_icon="🗄️", layout="wide")

st.title("🗄️ SQLite Database Viewer")
st.markdown("Upload your SQLite database file to inspect tables and run custom queries instantly.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose an SQLite database file (.db or .sqlite)", type=["db", "sqlite"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        db_path = temp_file.name

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("📋 Tables List")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]

            if tables:
                st.success(f"Found {len(tables)} table(s):")
                for table in tables:
                    st.markdown(f"- **`{table}`**")
                
                st.markdown("---")
                selected_table = st.selectbox("Quick preview a table:", tables)
            else:
                st.warning("No tables found in this database.")
                selected_table = None

        with col2:
            st.subheader("💻 Run Custom SQL Query")
            
            default_query = f"SELECT * FROM {tables[0]} LIMIT 5;" if tables else "SELECT * FROM table_name;"
            user_query = st.text_area("Write your SQL query below:", value=default_query, height=150)
            
            execute_btn = st.button("Execute Query 🚀", type="primary")

        if selected_table and not execute_btn:
            st.markdown("---")
            st.subheader(f"📊 Preview: `{selected_table}` (First 5 Rows)")
            preview_df = pd.read_sql_query(f"SELECT * FROM {selected_table} LIMIT 5;", conn)
            st.dataframe(preview_df, use_container_width=True)

        if execute_btn:
            st.markdown("---")
            if user_query.strip():
                try:
                    result_df = pd.read_sql_query(user_query, conn)
                    
                    st.success("Query executed successfully!")
                    st.subheader("📊 Result Dataframe")
                    st.dataframe(result_df, use_container_width=True)
                    
                    st.metric(label="Rows Returned", value=len(result_df))
                    
                except Exception as e:
                    st.error(f"❌ Error executing query: {e}")
            else:
                st.warning("Please write a query before executing.")

        conn.close()

    finally:
        if os.path.exists(db_path):
            os.remove(db_path)

else:
    st.info("ℹ️ Please upload an SQLite database file to get started.")