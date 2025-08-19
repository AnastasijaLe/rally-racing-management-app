import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Rally Racing Managment", page_icon="🏎")

# Initialize connection using st.connection
try:
    conn = st.connection("snowflake")
    st.title(" 🏎 Rally Racing Management")
    st.success("Connected to Snowflake! Ready to race! 🏁")

    # Example of how to use the connection to run a query
    # df = conn.query("SELECT CURRENT_VERSION()")
    # st.write(df)

except Exception as e:
    st.error(f"Failed to connect. Check your secrets and credentials. Error: {e}")