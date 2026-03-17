import streamlit as st
import pandas as pd

st.title("Operations & Logistics")

df = pd.read_csv("amazon_allyearclean.csv")

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("🚚 Delivery Performance Dashboard")


# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

# Data cleaning
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")

# Simulate delivery date if not available
if "delivery_date" not in df.columns:
    np.random.seed(42)
    df["delivery_days"] = np.random.randint(1,7,len(df))
    df["delivery_date"] = df["order_date"] + pd.to_timedelta(df["delivery_days"], unit="D")

# Calculate delivery time
df["delivery_time"] = (df["delivery_date"] - df["order_date"]).dt.days

# Define on-time delivery threshold (<=3 days)
df["on_time"] = df["delivery_time"].apply(lambda x: 1 if x <= 3 else 0)

# ---------------- DELIVERY TIME ANALYSIS ---------------- #

st.subheader("Average Delivery Time by Category")

delivery_time = (
    df.groupby("category")["delivery_time"]
    .mean()
    .reset_index()
)

fig1 = px.bar(
    delivery_time,
    x="category",
    y="delivery_time",
    title="Average Delivery Time by Category (Days)"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- ON-TIME DELIVERY RATE ---------------- #

st.subheader("On-Time Delivery Rate")

on_time_rate = df["on_time"].mean() * 100

st.metric("Overall On-Time Delivery Rate", f"{on_time_rate:.1f}%")

# ---------------- GEOGRAPHIC PERFORMANCE ---------------- #

st.subheader("Delivery Performance by State")

geo_perf = (
    df.groupby("customer_state")["delivery_time"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    geo_perf.sort_values("delivery_time"),
    x="customer_state",
    y="delivery_time",
    title="Average Delivery Time by State"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- DELIVERY VOLUME ---------------- #

st.subheader("Delivery Volume by Region")

delivery_vol = (
    df.groupby("customer_state")["product_id"]
    .count()
    .reset_index()
)

fig3 = px.bar(
    delivery_vol,
    x="customer_state",
    y="product_id",
    title="Orders Delivered by State"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- OPERATIONAL EFFICIENCY ---------------- #

st.subheader("Operational Efficiency Metrics")

avg_delivery = df["delivery_time"].mean()
fast_deliveries = (df["delivery_time"] <= 2).sum()
slow_deliveries = (df["delivery_time"] > 5).sum()

col1, col2, col3 = st.columns(3)

col1.metric("Average Delivery Time", f"{avg_delivery:.2f} Days")
col2.metric("Fast Deliveries (≤2 Days)", fast_deliveries)
col3.metric("Delayed Deliveries (>5 Days)", slow_deliveries)

# ---------------- DRILLDOWN ---------------- #

st.subheader("Delivery Trend Analysis")

df["month"] = df["order_date"].dt.month

monthly_delivery = df.groupby("month")["delivery_time"].mean().reset_index()

fig4 = px.line(
    monthly_delivery,
    x="month",
    y="delivery_time",
    markers=True,
    title="Monthly Delivery Time Trend"
)

st.plotly_chart(fig4, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("💳 Payment Analytics Dashboard")



# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

# Data Cleaning
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")

# Simulate payment methods if column not available
if "payment_method" not in df.columns:
    payment_types = ["UPI","Credit Card","Debit Card","Net Banking","Cash on Delivery"]
    np.random.seed(42)
    df["payment_method"] = np.random.choice(payment_types, size=len(df))

# Simulate transaction status if not available
if "payment_status" not in df.columns:
    df["payment_status"] = np.random.choice(["Success","Failed"], size=len(df), p=[0.95,0.05])

# ---------------- PAYMENT METHOD PREFERENCE ---------------- #

st.subheader("Payment Method Preference")

payment_pref = (
    df.groupby("payment_method")["product_id"]
    .count()
    .reset_index()
)

fig1 = px.pie(
    payment_pref,
    names="payment_method",
    values="product_id",
    title="Payment Method Distribution"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- TRANSACTION SUCCESS RATE ---------------- #

st.subheader("Transaction Success Rate")

success_rate = (
    df.groupby("payment_status")["product_id"]
    .count()
    .reset_index()
)

fig2 = px.pie(
    success_rate,
    names="payment_status",
    values="product_id",
    title="Payment Success vs Failure"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- PAYMENT REVENUE BY METHOD ---------------- #

st.subheader("Revenue by Payment Method")

payment_rev = (
    df.groupby("payment_method")["final_amount_inr"]
    .sum()
    .reset_index()
)

fig3 = px.bar(
    payment_rev,
    x="payment_method",
    y="final_amount_inr",
    title="Revenue Contribution by Payment Method"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- PAYMENT TREND EVOLUTION ---------------- #

st.subheader("Payment Trends Over Time")

df["month"] = df["order_date"].dt.month
payment_trend = (
    df.groupby(["month","payment_method"])["final_amount_inr"]
    .sum()
    .reset_index()
)

fig4 = px.line(
    payment_trend,
    x="month",
    y="final_amount_inr",
    color="payment_method",
    title="Monthly Payment Method Trends"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- FINANCIAL INSIGHTS ---------------- #

st.subheader("Financial Payment Insights")

total_transactions = len(df)
successful = len(df[df["payment_status"]=="Success"])
failed = len(df[df["payment_status"]=="Failed"])

col1, col2, col3 = st.columns(3)

col1.metric("Total Transactions", total_transactions)
col2.metric("Successful Payments", successful)
col3.metric("Failed Transactions", failed)

# ---------------- PAYMENT METHOD DRILLDOWN ---------------- #

st.subheader("Payment Method Drilldown")

method_select = st.selectbox(
    "Select Payment Method",
    df["payment_method"].unique()
)

method_data = df[df["payment_method"] == method_select]

monthly_sales = method_data.groupby("month")["final_amount_inr"].sum().reset_index()

fig5 = px.line(
    monthly_sales,
    x="month",
    y="final_amount_inr",
    markers=True,
    title=f"Revenue Trend for {method_select}"
)

st.plotly_chart(fig5, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("🚚 Supply Chain Dashboard")



# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

# Data cleaning
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# Simulate supplier column if not present
if "supplier" not in df.columns:
    suppliers = ["Vendor A", "Vendor B", "Vendor C", "Vendor D", "Vendor E"]
    np.random.seed(42)
    df["supplier"] = np.random.choice(suppliers, size=len(df))

# Simulate delivery time if not present
if "delivery_days" not in df.columns:
    df["delivery_days"] = np.random.randint(2,7,len(df))

# ---------------- SUPPLIER PERFORMANCE ---------------- #

st.subheader("Supplier Performance by Revenue")

supplier_perf = (
    df.groupby("supplier")["final_amount_inr"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    supplier_perf,
    x="supplier",
    y="final_amount_inr",
    title="Revenue Contribution by Supplier"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- DELIVERY RELIABILITY ---------------- #

st.subheader("Delivery Reliability")
df["delivery_days"] = pd.to_numeric(df["delivery_days"], errors="coerce")

delivery_rel = (
    df.groupby("supplier")["delivery_days"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    delivery_rel,
    x="supplier",
    y="delivery_days",
    title="Average Delivery Time by Supplier"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- COST ANALYSIS ---------------- #

st.subheader("Supply Cost Analysis")

cost_analysis = (
    df.groupby("supplier")["final_amount_inr"]
    .mean()
    .reset_index()
)

fig3 = px.bar(
    cost_analysis,
    x="supplier",
    y="final_amount_inr",
    title="Average Order Value by Supplier"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- SUPPLIER ORDER VOLUME ---------------- #

st.subheader("Supplier Order Volume")

order_volume = (
    df.groupby("supplier")["product_id"]
    .count()
    .reset_index()
)

fig4 = px.pie(
    order_volume,
    names="supplier",
    values="product_id",
    title="Supplier Order Share"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- SUPPLY CHAIN METRICS ---------------- #

st.subheader("Supply Chain Efficiency Metrics")

avg_delivery = df["delivery_days"].mean()
total_orders = df["product_id"].count()
total_suppliers = df["supplier"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Average Delivery Days", f"{avg_delivery:.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Active Suppliers", total_suppliers)

# ---------------- SUPPLIER DRILLDOWN ---------------- #

st.subheader("Supplier Drilldown Analysis")

supplier_select = st.selectbox(
    "Select Supplier",
    df["supplier"].unique()
)

supplier_data = df[df["supplier"] == supplier_select]

monthly_perf = (
    supplier_data.groupby(df["order_date"].dt.month)["final_amount_inr"]
    .sum()
    .reset_index()
)

fig5 = px.line(
    monthly_perf,
    x="order_date",
    y="final_amount_inr",
    markers=True,
    title=f"Monthly Revenue for {supplier_select}"
)

st.plotly_chart(fig5, use_container_width=True)

