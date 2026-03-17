import streamlit as st
import pandas as pd

st.title("Executive Summary Dashboard")

df = pd.read_csv("amazon_allyearclean.csv")
df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')
# Q1 Key Metrics
st.header("Key Business Metrics")

total_revenue = df['final_amount_inr'].sum()
active_customers = df['customer_id'].nunique()
aov = df['final_amount_inr'].mean()

st.metric("Total Revenue", f"₹{total_revenue:,.0f}")
st.metric("Active Customers", active_customers)
st.metric("Average Order Value", f"₹{aov:,.0f}")

# Top Categories
st.subheader("Top Performing Categories")

cat = df.groupby("category")["final_amount_inr"].sum().sort_values(ascending=False)
st.bar_chart(cat)

# Q2 Real Time Monitor
st.header("Real Time Performance")

monthly = df.groupby("order_month")["final_amount_inr"].sum()
st.line_chart(monthly)

# Q3 Strategic Overview
st.header("Market Overview")

state = df.groupby("customer_state")["final_amount_inr"].sum()
st.bar_chart(state)

# Q4 Financial Performance
st.header("Revenue by Category")

st.bar_chart(df.groupby("category")["final_amount_inr"].sum())

# Q5 Growth Analytics
st.header("Customer Growth")

customers = df.groupby("order_year")["customer_id"].nunique()
st.line_chart(customers)

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Executive Summary Dashboard")

# Load Data
df = pd.read_csv("amazon_allyearclean.csv")

# Convert Date
df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')
# Create Year Column
df['year'] = df['order_date'].dt.year

# ---------------- KPI CALCULATIONS ---------------- #

total_revenue = df["final_amount_inr"].sum()

active_customers = df["customer_id"].nunique()

avg_order_value = df["final_amount_inr"].mean()

# Yearly revenue
yearly_rev = df.groupby("year")["final_amount_inr"].sum().reset_index()

# Growth rate
growth_rate = yearly_rev["final_amount_inr"].pct_change().iloc[-1] * 100

# Top categories
top_categories = (
    df.groupby("category")["final_amount_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

# ---------------- KPI CARDS ---------------- #

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"₹{total_revenue:,.0f}"
)

col2.metric(
    "Growth Rate",
    f"{growth_rate:.2f}%"
)

col3.metric(
    "Active Customers",
    active_customers
)

col4.metric(
    "Average Order Value",
    f"₹{avg_order_value:.0f}"
)

# ---------------- REVENUE TREND ---------------- #

st.subheader("Revenue Trend (Year over Year)")

fig1 = px.line(
    yearly_rev,
    x="year",
    y="final_amount_inr",
    markers=True,
    title="Yearly Revenue Growth"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- TOP CATEGORIES ---------------- #

st.subheader("Top Performing Categories")

fig2 = px.bar(
    top_categories,
    x="category",
    y="final_amount_inr",
    title="Top Revenue Categories"
)

st.plotly_chart(fig2, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.title("⚡ Real-time Business Performance Monitor")

# Load Data
df = pd.read_csv("amazon_allyearclean.csv")

df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month

today = datetime.today()

current_year = today.year
current_month = today.month

# Filter Current Month Data
current_month_df = df[
    (df["year"] == current_year) &
    (df["month"] == current_month)
]

# ---------------- TARGETS ---------------- #

monthly_revenue_target = 500000
customer_target = 300

# ---------------- KPI CALCULATIONS ---------------- #

current_revenue = current_month_df["final_amount_inr"].sum()

active_customers = current_month_df["customer_id"].nunique()

orders = current_month_df["transaction_id"].nunique()

days_passed = today.day

run_rate = (current_revenue / days_passed) * 30

avg_order_value = current_month_df["final_amount_inr"].mean()

# ---------------- KPI CARDS ---------------- #

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Month Revenue",
    f"₹{current_revenue:,.0f}"
)

col2.metric(
    "Revenue Run Rate",
    f"₹{run_rate:,.0f}"
)

col3.metric(
    "New Customers",
    active_customers
)

col4.metric(
    "Average Order Value",
    f"₹{avg_order_value:.0f}"
)

# ---------------- TARGET COMPARISON ---------------- #

st.subheader("Performance vs Targets")

revenue_progress = (current_revenue / monthly_revenue_target) * 100
customer_progress = (active_customers / customer_target) * 100

st.progress(int(min(revenue_progress,100)))
st.write(f"Revenue Target Progress: {revenue_progress:.1f}%")

st.progress(int(min(customer_progress,100)))
st.write(f"Customer Target Progress: {customer_progress:.1f}%")

# ---------------- REVENUE TREND ---------------- #

st.subheader("Daily Revenue Trend")

daily_rev = current_month_df.groupby("order_date")["final_amount_inr"].sum().reset_index()

fig = px.line(
    daily_rev,
    x="order_date",
    y="final_amount_inr",
    title="Current Month Revenue Trend"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- OPERATIONAL METRICS ---------------- #

st.subheader("Operational Indicators")

avg_delivery = current_month_df["delivery_days"].mean()

returns = current_month_df["return_status"].value_counts().get("Returned",0)

col5, col6 = st.columns(2)

col5.metric("Avg Delivery Days", f"{avg_delivery:.1f}")

col6.metric("Returns This Month", returns)

# ---------------- ALERT SYSTEM ---------------- #

st.subheader("⚠ Performance Alerts")

if revenue_progress < 70:
    st.error("Revenue performance below 70% of target")

elif revenue_progress < 90:
    st.warning("Revenue slightly below target")

else:
    st.success("Revenue target on track")

if customer_progress < 70:
    st.error("Customer acquisition below target")

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Strategic Overview Dashboard")
st.markdown("Executive level insights for strategic decision making")

# Load Data
df = pd.read_csv("amazon_allyearclean.csv")

df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')
df["year"] = df["order_date"].dt.year

# ---------------- BUSINESS HEALTH KPIs ---------------- #

total_revenue = df["final_amount_inr"].sum()
total_customers = df["customer_id"].nunique()
total_orders = df["transaction_id"].nunique()
avg_order_value = df["final_amount_inr"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Customers", total_customers)
col3.metric("Total Orders", total_orders)
col4.metric("Avg Order Value", f"₹{avg_order_value:.0f}")

# ---------------- MARKET SHARE ANALYSIS ---------------- #

st.subheader("Market Share by Category")

category_share = (
    df.groupby("category")["final_amount_inr"]
    .sum()
    .reset_index()
)

fig1 = px.pie(
    category_share,
    names="category",
    values="final_amount_inr",
    title="Revenue Share by Product Category"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- COMPETITIVE POSITIONING ---------------- #

st.subheader("Competitive Positioning (Top Brands)")

brand_rev = (
    df.groupby("brand")["final_amount_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    brand_rev,
    x="brand",
    y="final_amount_inr",
    title="Top Brands by Revenue"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- GEOGRAPHIC EXPANSION ---------------- #

st.subheader("Geographic Revenue Distribution")

city_rev = (
    df.groupby("customer_city")["final_amount_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    city_rev,
    x="customer_city",
    y="final_amount_inr",
    title="Top Cities by Revenue"
)

st.plotly_chart(fig3, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("💰 Financial Performance Dashboard")

# Load Data
df = pd.read_csv("amazon_allyearclean.csv")

df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')

df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month

# Ensure numeric values
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")
df["original_price_inr"] = pd.to_numeric(df["original_price_inr"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# ---------------- PROFIT CALCULATION ---------------- #

# Assume cost is 70% of price if actual cost not available
df["cost"] = df["original_price_inr"] * df["quantity"] * 0.7

df["revenue"] = df["final_amount_inr"]

df["profit"] = df["revenue"] - df["cost"]

df["profit_margin"] = (df["profit"] / df["revenue"]) * 100

# ---------------- KPI METRICS ---------------- #

total_revenue = df["revenue"].sum()
total_profit = df["profit"].sum()
avg_margin = df["profit_margin"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Average Profit Margin", f"{avg_margin:.2f}%")

# ---------------- REVENUE BY CATEGORY ---------------- #

st.subheader("Revenue Breakdown by Category")

category_rev = (
    df.groupby("category")["revenue"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    category_rev,
    x="category",
    y="revenue",
    title="Revenue by Product Category"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- PROFIT MARGIN ANALYSIS ---------------- #

st.subheader("Profit Margin by Category")

margin_cat = (
    df.groupby("category")["profit_margin"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    margin_cat,
    x="category",
    y="profit_margin",
    title="Average Profit Margin"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- COST STRUCTURE ---------------- #

st.subheader("Cost Structure")

cost_data = pd.DataFrame({
    "Type": ["Revenue", "Cost", "Profit"],
    "Value": [total_revenue, df["cost"].sum(), total_profit]
})

fig3 = px.pie(
    cost_data,
    names="Type",
    values="Value",
    title="Financial Cost Structure"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- REVENUE FORECAST ---------------- #

st.subheader("Revenue Forecast (Simple Trend Model)")

monthly_rev = (
    df.groupby(["year","month"])["revenue"]
    .sum()
    .reset_index()
)

monthly_rev["time_index"] = range(len(monthly_rev))

# simple linear regression forecast
coeff = np.polyfit(monthly_rev["time_index"], monthly_rev["revenue"], 1)

trend = np.poly1d(coeff)

monthly_rev["forecast"] = trend(monthly_rev["time_index"])

fig4 = px.line(
    monthly_rev,
    x="time_index",
    y=["revenue","forecast"],
    title="Revenue Forecast Trend"
)

st.plotly_chart(fig4, use_container_width=True)
