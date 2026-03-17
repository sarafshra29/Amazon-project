import streamlit as st
import pandas as pd


st.set_page_config(page_title="Amazon Business Overview", layout="wide")

st.title("📦 Amazon Business Overview Dashboard")

page = st.sidebar.radio(
    "Select Page",
    [
        "Executive Dashboard",
        "Revenue Analytics",
        "Customer Analytics",
        "Product Inventory",
        "Operations Logistics",
        "Advanced Analytics"
    ]
)

# PAGE ROUTING
if page == "Executive Dashboard":
    import Executivedashboard

elif page == "Revenue Analytics":
    import RevenueAnalytics

elif page == "Customer Analytics":
    import CustomerAnalytics

elif page == "Product Inventory":
    import ProductInventory

elif page == "Operations Logistics":
    import OperationLogistic

elif page == "Advanced Analytics":
    import Advancedanalytics






