import streamlit as st
import pandas as pd
import plotly.express as px

st.title("💰 Revenue Trend Analysis Dashboard")

st.write("This is the Revenue Analytics Page")

df = pd.read_csv("amazon_allyearclean.csv")

df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month

monthly_rev = df.groupby("month")["final_amount_inr"].sum().reset_index()

fig = px.line(
    monthly_rev,
    x="month",
    y="final_amount_inr",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("💰 Revenue Trend Analysis Dashboard")



# Load data
df = pd.read_csv("amazon_allyearclean.csv")

df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')

df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["quarter"] = df["order_date"].dt.quarter

df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")

# ---------------- TIME PERIOD SELECTOR ---------------- #

period = st.selectbox(
    "Select Revenue Time Period",
    ["Monthly", "Quarterly", "Yearly"]
)

# ---------------- AGGREGATE REVENUE ---------------- #

if period == "Monthly":

    revenue = df.groupby(["year","month"])["final_amount_inr"].sum().reset_index()
    revenue["time"] = revenue["year"].astype(str) + "-" + revenue["month"].astype(str)

elif period == "Quarterly":

    revenue = df.groupby(["year","quarter"])["final_amount_inr"].sum().reset_index()
    revenue["time"] = revenue["year"].astype(str) + "-Q" + revenue["quarter"].astype(str)

else:

    revenue = df.groupby("year")["final_amount_inr"].sum().reset_index()
    revenue["time"] = revenue["year"]

# ---------------- REVENUE TREND ---------------- #

st.subheader("Revenue Trend")

fig1 = px.line(
    revenue,
    x="time",
    y="final_amount_inr",
    markers=True,
    title=f"{period} Revenue Trend"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- GROWTH RATE ---------------- #

revenue["growth_rate"] = revenue["final_amount_inr"].pct_change() * 100

st.subheader("Growth Rate (%)")

fig2 = px.bar(
    revenue,
    x="time",
    y="growth_rate",
    title="Revenue Growth Rate"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- SEASONAL VARIATION ---------------- #

st.subheader("Seasonal Revenue Pattern")

seasonal = df.groupby("month")["final_amount_inr"].sum().reset_index()

fig3 = px.line(
    seasonal,
    x="month",
    y="final_amount_inr",
    markers=True,
    title="Monthly Seasonal Pattern"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- FORECASTING ---------------- #

st.subheader("Revenue Forecast")

revenue["time_index"] = range(len(revenue))

coeff = np.polyfit(revenue["time_index"], revenue["final_amount_inr"], 1)

trend = np.poly1d(coeff)

revenue["forecast"] = trend(revenue["time_index"])

fig4 = px.line(
    revenue,
    x="time",
    y=["final_amount_inr","forecast"],
    title="Revenue Forecast Trend"
)

st.plotly_chart(fig4, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📦 Category Performance Dashboard")



# Load data
df = pd.read_csv("amazon_allyearclean.csv")

df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')

df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month

df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")
df["original_price_inr"] = pd.to_numeric(df["original_price_inr"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# ---------------- PROFIT CALCULATION ---------------- #

df["cost"] = df["original_price_inr"] * df["quantity"] * 0.7
df["revenue"] = df["final_amount_inr"]
df["profit"] = df["revenue"] - df["cost"]

# ---------------- REVENUE CONTRIBUTION ---------------- #

st.subheader("Revenue Contribution by Category")

category_rev = df.groupby("category")["revenue"].sum().reset_index()

fig1 = px.pie(
    category_rev,
    names="category",
    values="revenue",
    title="Category Revenue Share"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- GROWTH TREND ---------------- #

st.subheader("Category Growth Trend")

cat_growth = df.groupby(["year","category"])["revenue"].sum().reset_index()

fig2 = px.line(
    cat_growth,
    x="year",
    y="revenue",
    color="category",
    markers=True,
    title="Category Revenue Growth"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- MARKET SHARE ---------------- #

st.subheader("Market Share by Category")

total_rev = df["revenue"].sum()

category_rev["market_share_%"] = (category_rev["revenue"] / total_rev) * 100

fig3 = px.bar(
    category_rev,
    x="category",
    y="market_share_%",
    title="Category Market Share (%)"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- CATEGORY PROFITABILITY ---------------- #

st.subheader("Category Profitability")

profit_cat = df.groupby("category")["profit"].sum().reset_index()

fig4 = px.bar(
    profit_cat,
    x="category",
    y="profit",
    title="Profit by Category"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- DRILL-DOWN FEATURE ---------------- #

st.subheader("Product Drill-down")

selected_category = st.selectbox(
    "Select Category",
    df["category"].unique()
)

product_data = df[df["category"] == selected_category]

top_products = (
    product_data.groupby("product_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig5 = px.bar(
    top_products,
    x="product_name",
    y="revenue",
    title=f"Top Products in {selected_category}"
)

st.plotly_chart(fig5, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌍 Geographic Revenue Analysis Dashboard")


# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

# Convert date
df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')

df["year"] = df["order_date"].dt.year

df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")

# ---------------- STATE REVENUE ---------------- #

st.subheader("State-wise Revenue Performance")

state_rev = df.groupby("customer_state")["final_amount_inr"].sum().reset_index()

fig1 = px.bar(
    state_rev.sort_values("final_amount_inr", ascending=False),
    x="customer_state",
    y="final_amount_inr",
    title="Revenue by State"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- CITY PERFORMANCE ---------------- #

st.subheader("Top Cities by Revenue")

city_rev = df.groupby("customer_city")["final_amount_inr"].sum().reset_index()

top_cities = city_rev.sort_values("final_amount_inr", ascending=False).head(15)

fig2 = px.bar(
    top_cities,
    x="customer_city",
    y="final_amount_inr",
    title="Top Revenue Generating Cities"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- TIER ANALYSIS ---------------- #

st.subheader("Tier-wise Revenue Growth")

tier_mapping = {
    "Mumbai":"Tier 1","Delhi":"Tier 1","Bangalore":"Tier 1",
    "Hyderabad":"Tier 1","Chennai":"Tier 1",
    "Pune":"Tier 2","Ahmedabad":"Tier 2","Jaipur":"Tier 2",
}

df["city_tier"] = df["customer_city"].map(tier_mapping).fillna("Tier 3")

tier_rev = df.groupby("city_tier")["final_amount_inr"].sum().reset_index()

fig3 = px.pie(
    tier_rev,
    names="city_tier",
    values="final_amount_inr",
    title="Revenue Contribution by City Tier"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- MARKET PENETRATION ---------------- #

st.subheader("Market Penetration Opportunities")

orders_by_state = df.groupby("customer_state")["product_id"].count().reset_index()

orders_by_state = orders_by_state.sort_values("product_id")

fig4 = px.bar(
    orders_by_state,
    x="customer_state",
    y="product_id",
    title="Product Volume by State (Low volume = Opportunity)"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- INTERACTIVE MAP ---------------- #

st.subheader("Interactive Revenue Map")

fig5 = px.scatter_geo(
    state_rev,
    locations="customer_state",
    locationmode="country names",
    size="final_amount_inr",
    title="Geographic Revenue Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🎉 Festival Sales Analytics Dashboard")



# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')

df["month"] = df["order_date"].dt.month
df["year"] = df["order_date"].dt.year

df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")
df["original_price_inr"] = pd.to_numeric(df["original_price_inr"], errors="coerce")

# ---------------- FESTIVAL MAPPING ---------------- #

festival_map = {
    1: "New Year",
    2: "Valentine",
    3: "Holi",
    8: "Independence Sale",
    9: "Ganesh Chaturthi",
    10: "Diwali",
    11: "Black Friday",
    12: "Christmas"
}

df["festival"] = df["month"].map(festival_map).fillna("Regular Days")

# ---------------- FESTIVAL REVENUE ---------------- #

st.subheader("Festival Revenue Performance")

festival_rev = df.groupby("festival")["final_amount_inr"].sum().reset_index()

fig1 = px.bar(
    festival_rev.sort_values("final_amount_inr", ascending=False),
    x="festival",
    y="final_amount_inr",
    title="Revenue by Festival"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- CAMPAIGN EFFECTIVENESS ---------------- #

st.subheader("Campaign Effectiveness")

df["discount"] = df["original_price_inr"] - df["final_amount_inr"]

campaign_perf = df.groupby("festival")["discount"].sum().reset_index()

fig2 = px.bar(
    campaign_perf,
    x="festival",
    y="discount",
    title="Total Promotional Discounts by Festival"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- PROMOTION IMPACT ---------------- #

st.subheader("Promotion Impact on Revenue")

promo_analysis = df.groupby(["festival"])["final_amount_inr"].mean().reset_index()

fig3 = px.line(
    promo_analysis,
    x="festival",
    y="final_amount_inr",
    markers=True,
    title="Average Order Value During Festivals"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- SEASONAL TREND ---------------- #

st.subheader("Seasonal Revenue Pattern")

monthly_rev = df.groupby("month")["final_amount_inr"].sum().reset_index()

fig4 = px.line(
    monthly_rev,
    x="month",
    y="final_amount_inr",
    markers=True,
    title="Monthly Seasonal Revenue Trend"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- FESTIVAL FILTER ---------------- #

st.subheader("Festival Drill-down")

festival_select = st.selectbox(
    "Select Festival",
    df["festival"].unique()
)

festival_data = df[df["festival"] == festival_select]

top_products = (
    festival_data.groupby("product_name")["final_amount_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig5 = px.bar(
    top_products,
    x="product_name",
    y="final_amount_inr",
    title=f"Top Products During {festival_select}"
)

st.plotly_chart(fig5, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("💰 Price Optimization Dashboard")


# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")
df["original_price_inr"] = pd.to_numeric(df["original_price_inr"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# ---------------- DISCOUNT CALCULATION ---------------- #

df["discount"] = df["original_price_inr"] - df["final_amount_inr"]
df["discount_percent"] = (df["discount"] / df["original_price_inr"]) * 100

# ---------------- PRICE ELASTICITY ---------------- #

st.subheader("Price Elasticity Analysis")

elasticity_data = df.groupby("final_amount_inr")["quantity"].sum().reset_index()

fig1 = px.scatter(
    elasticity_data,
    x="final_amount_inr",
    y="quantity",
    title="Price vs Demand Relationship"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- DISCOUNT EFFECTIVENESS ---------------- #

st.subheader("Discount Effectiveness")

discount_perf = df.groupby("discount_percent")["final_amount_inr"].sum().reset_index()

fig2 = px.scatter(
    discount_perf,
    x="discount_percent",
    y="final_amount_inr",
    title="Discount Percentage vs Revenue")

st.plotly_chart(fig2, use_container_width=True)

# ---------------- COMPETITIVE PRICING ---------------- #

st.subheader("Competitive Pricing Comparison")

price_comp = df.groupby("category")[["original_price_inr","final_amount_inr"]].mean().reset_index()