import streamlit as st
import snowflake.connector
import pandas as pd

# page config
st.set_page_config(page_title="Rally Racing Managment", page_icon="🏎")

# snowflake connection using sidebar
st.sidebar.header("Snowflake connection")
account = st.sidebar.text_input("Account", placeholder="xy12345.us-east-1")
user = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
role = st.sidebar.text_input("Role", value="SYSADMIN")
warehouse = st.sidebar.text_input("Warehouse", value="COMPUTE_WH")
database = st.sidebar.text_input("Database", value= "BOOTCAMP_RALLY")

@st.cache_resource
def init_connection():
    try:
        conn = snowflake.connector.connect(
            user = user,
            password = password,
            account = account,
            role = role,
            warehouse = warehouse,
            database = database
        )
        st.sidebar.success("Connected to Snowflake!")
        return conn
    except Exception as e:
        st.sidebar.error(f"Connection failed: {e}")
        return None
    
# initializing connection
if user and password and account:
    conn = init_connection()

    if conn:
        st.title(" 🏎 Rally Racing Managment")
        st.success("Connected to snowflake! Ready to race! 🏁")

else:
    st.warning("Please enter Snowflake connection details in the sidebar")