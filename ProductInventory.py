import streamlit as st
import pandas as pd

st.title("Product & Inventory Analytics")

df = pd.read_csv("amazon_allyearclean.csv")



import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np



# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")


df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")

num_cols = [
    "final_amount_inr",
    "original_price_inr",
    "quantity",
    "customer_rating"
]

for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Data cleaning
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# Simulate ratings if not available
if "customer_rating" not in df.columns:
    np.random.seed(42)
    df["customer_rating"] = np.random.uniform(3,5,len(df))

# Simulate return flag
if "returned" not in df.columns:
    df["returned"] = np.random.choice([0,1], size=len(df), p=[0.9,0.1])

# ---------------- PRODUCT PERFORMANCE ---------------- #

st.subheader("Top Products by Revenue")

product_rev = (
    df.groupby("product_name")["final_amount_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig1 = px.bar(
    product_rev,
    x="product_name",
    y="final_amount_inr",
    title="Top 10 Products by Revenue"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- UNITS SOLD ---------------- #

st.subheader("Top Products by Units Sold")

units = (
    df.groupby("product_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    units,
    x="product_name",
    y="quantity",
    title="Top Products by Units Sold"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- PRODUCT RATINGS ---------------- #

st.subheader("Product Ratings")

ratings = (
    df.groupby("product_name")["customer_rating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    ratings,
    x="product_name",
    y="customer_rating",
    title="Top Rated Products"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- RETURN RATE ---------------- #

st.subheader("Return Rate by Product")

returns = (
    df.groupby("product_name")["returned"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4 = px.bar(
    returns,
    x="product_name",
    y="returned",
    title="Products with Highest Return Rate"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- CATEGORY PERFORMANCE ---------------- #

st.subheader("Category-wise Revenue")

category_rev = df.groupby("category")["final_amount_inr"].sum().reset_index()

fig5 = px.pie(
    category_rev,
    names="category",
    values="final_amount_inr",
    title="Revenue Share by Category"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------- PRODUCT LIFECYCLE ---------------- #

st.subheader("Product Lifecycle Trend")

df["year"] = df["order_date"].dt.year

lifecycle = df.groupby(["year","product_name"])["final_amount_inr"].sum().reset_index()

top_products = lifecycle["product_name"].value_counts().head(5).index

lifecycle = lifecycle[lifecycle["product_name"].isin(top_products)]

fig6 = px.line(
    lifecycle,
    x="year",
    y="final_amount_inr",
    color="product_name",
    title="Revenue Lifecycle of Top Products"
)

st.plotly_chart(fig6, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏷️ Brand Analytics Dashboard")



# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

# Data cleaning
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# If brand column not available, simulate from product name
if "brand" not in df.columns:
    df["brand"] = df["product_name"].str.split().str[0]

# ---------------- BRAND REVENUE PERFORMANCE ---------------- #

st.subheader("Top Brands by Revenue")

brand_rev = (
    df.groupby("brand")["final_amount_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig1 = px.bar(
    brand_rev,
    x="brand",
    y="final_amount_inr",
    title="Top 10 Brands by Revenue"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- BRAND MARKET SHARE ---------------- #

st.subheader("Brand Market Share")

brand_share = df.groupby("brand")["final_amount_inr"].sum().reset_index()

fig2 = px.pie(
    brand_share,
    names="brand",
    values="final_amount_inr",
    title="Brand Revenue Market Share"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- BRAND PERFORMANCE OVER TIME ---------------- #

st.subheader("Brand Market Share Evolution")

df["year"] = df["order_date"].dt.year

brand_trend = (
    df.groupby(["year","brand"])["final_amount_inr"]
    .sum()
    .reset_index()
)

top_brands = brand_trend.groupby("brand")["final_amount_inr"].sum().nlargest(5).index
brand_trend = brand_trend[brand_trend["brand"].isin(top_brands)]

fig3 = px.line(
    brand_trend,
    x="year",
    y="final_amount_inr",
    color="brand",
    title="Revenue Trend of Top Brands"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- CATEGORY COMPETITION ---------------- #

st.subheader("Brand Competition Across Categories")

category_brand = (
    df.groupby(["category","brand"])["final_amount_inr"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    category_brand,
    x="category",
    y="final_amount_inr",
    color="brand",
    title="Brand Performance by Category"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- CUSTOMER BRAND PREFERENCE ---------------- #

st.subheader("Customer Brand Preference")

customer_brand = (
    df.groupby(["customer_id","brand"])["final_amount_inr"]
    .sum()
    .reset_index()
)

pref = customer_brand.groupby("brand")["customer_id"].nunique().reset_index()

fig5 = px.bar(
    pref.sort_values("customer_id", ascending=False).head(10),
    x="brand",
    y="customer_id",
    title="Brands with Most Unique Customers"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------- BRAND DRILLDOWN ---------------- #

st.subheader("Brand Drilldown")

brand_select = st.selectbox(
    "Select Brand",
    df["brand"].unique()
)

brand_data = df[df["brand"] == brand_select]

st.metric("Total Revenue", f"₹{brand_data['final_amount_inr'].sum():,.0f}")
st.metric("Units Sold", int(brand_data["quantity"].sum()))

top_products = (
    brand_data.groupby("product_name")["final_amount_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig6 = px.bar(
    top_products,
    x="product_name",
    y="final_amount_inr",
    title=f"Top Products of {brand_select}"
)

st.plotly_chart(fig6, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("📦 Inventory Optimization Dashboard")


# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

# Data cleaning
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")

df["month"] = df["order_date"].dt.month
df["year"] = df["order_date"].dt.year

# ---------------- PRODUCT DEMAND PATTERN ---------------- #

st.subheader("Top Products by Demand")

demand = (
    df.groupby("product_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig1 = px.bar(
    demand,
    x="product_name",
    y="quantity",
    title="Top 10 Products by Units Sold"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- SEASONAL DEMAND TREND ---------------- #

st.subheader("Seasonal Demand Trend")

seasonal = df.groupby("month")["quantity"].sum().reset_index()

fig2 = px.line(
    seasonal,
    x="month",
    y="quantity",
    markers=True,
    title="Monthly Demand Trend"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- INVENTORY TURNOVER ---------------- #

st.subheader("Inventory Turnover by Category")

turnover = (
    df.groupby("category")["quantity"]
    .sum()
    .reset_index()
)

fig3 = px.bar(
    turnover,
    x="category",
    y="quantity",
    title="Category-wise Inventory Turnover"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- DEMAND FORECASTING ---------------- #

st.subheader("Demand Forecasting")

monthly_demand = df.groupby(["year","month"])["quantity"].sum().reset_index()

monthly_demand["time_index"] = range(len(monthly_demand))

# Simple trend forecasting
coeff = np.polyfit(monthly_demand["time_index"], monthly_demand["quantity"], 1)
trend = np.poly1d(coeff)

monthly_demand["forecast"] = trend(monthly_demand["time_index"])

fig4 = px.line(
    monthly_demand,
    x="time_index",
    y=["quantity","forecast"],
    title="Demand Forecast Trend"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- LOW DEMAND PRODUCTS ---------------- #

st.subheader("Low Demand Products (Inventory Risk)")

low_demand = (
    df.groupby("product_name")["quantity"]
    .sum()
    .sort_values()
    .head(10)
    .reset_index()
)

fig5 = px.bar(
    low_demand,
    x="product_name",
    y="quantity",
    title="Products with Lowest Demand"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------- PRODUCT FILTER ---------------- #

st.subheader("Product Demand Drilldown")

product_select = st.selectbox(
    "Select Product",
    df["product_name"].unique()
)

product_data = df[df["product_name"] == product_select]

monthly_product = product_data.groupby("month")["quantity"].sum().reset_index()

fig6 = px.line(
    monthly_product,
    x="month",
    y="quantity",
    markers=True,
    title=f"Demand Trend for {product_select}"
)

st.plotly_chart(fig6, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("🚀 New Product Launch Dashboard")


# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

# Data cleaning
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

df["year"] = df["order_date"].dt.year

# ---------------- IDENTIFY NEW PRODUCTS ---------------- #

first_sale = df.groupby("product_name")["order_date"].min().reset_index()
first_sale.columns = ["product_name", "launch_date"]

df = df.merge(first_sale, on="product_name")

# Consider products launched in latest year as new
latest_year = df["year"].max()
df["is_new_product"] = df["launch_date"].dt.year == latest_year

new_products = df[df["is_new_product"] == True]

# ---------------- LAUNCH PERFORMANCE ---------------- #

st.subheader("Top New Products by Revenue")

launch_perf = (
    new_products.groupby("product_name")["final_amount_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig1 = px.bar(
    launch_perf,
    x="product_name",
    y="final_amount_inr",
    title="Top New Products by Revenue"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- MARKET ACCEPTANCE ---------------- #

st.subheader("Market Acceptance (Units Sold)")

acceptance = (
    new_products.groupby("product_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    acceptance,
    x="product_name",
    y="quantity",
    title="Units Sold for New Products"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- CATEGORY COMPETITION ---------------- #

st.subheader("New Product Competition by Category")

category_perf = (
    new_products.groupby("category")["final_amount_inr"]
    .sum()
    .reset_index()
)

fig3 = px.pie(
    category_perf,
    names="category",
    values="final_amount_inr",
    title="New Product Revenue by Category"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- SUCCESS METRICS ---------------- #

st.subheader("Launch Success Metrics")

total_new_products = new_products["product_name"].nunique()
total_revenue = new_products["final_amount_inr"].sum()
avg_sales = new_products.groupby("product_name")["quantity"].sum().mean()

col1, col2, col3 = st.columns(3)

col1.metric("New Products Launched", total_new_products)
col2.metric("Total Launch Revenue", f"₹{total_revenue:,.0f}")
col3.metric("Avg Units Sold per Product", int(avg_sales))

# ---------------- PRODUCT DRILLDOWN ---------------- #

st.subheader("New Product Performance Drilldown")

product_select = st.selectbox(
    "Select New Product",
    new_products["product_name"].unique()
)

product_data = new_products[new_products["product_name"] == product_select]

monthly_sales = product_data.groupby("year")["final_amount_inr"].sum().reset_index()

fig4 = px.line(
    monthly_sales,
    x="year",
    y="final_amount_inr",
    markers=True,
    title=f"Revenue Trend for {product_select}"
)

st.plotly_chart(fig4, use_container_width=True)