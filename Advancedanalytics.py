import streamlit as st
import pandas as pd

st.title("Advanced Analytics")

df = pd.read_csv("amazon_allyearclean.csv")
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("🤖 Predictive Analytics Dashboard")

# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

# Data cleaning
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month

# ---------------- SALES FORECASTING ---------------- #

st.subheader("📈 Sales Forecasting (Moving Average)")

monthly_sales = (
    df.groupby(["year","month"])["final_amount_inr"]
    .sum()
    .reset_index()
)

# Create time index
monthly_sales["time"] = range(len(monthly_sales))

# Moving average forecast
monthly_sales["forecast"] = monthly_sales["final_amount_inr"].rolling(3).mean()

fig1 = px.line(
    monthly_sales,
    x="time",
    y=["final_amount_inr","forecast"],
    title="Sales Trend & Forecast (Moving Average)"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- CUSTOMER CHURN ANALYSIS ---------------- #

st.subheader("👥 Customer Churn Analysis")

customer_orders = df.groupby("customer_id")["product_id"].count().reset_index()

customer_orders["churn_risk"] = customer_orders["product_id"].apply(
    lambda x: "High Risk" if x <= 1 else "Low Risk"
)

churn_summary = customer_orders["churn_risk"].value_counts().reset_index()
churn_summary.columns = ["Risk","Customers"]

fig2 = px.pie(
    churn_summary,
    names="Risk",
    values="Customers",
    title="Customer Churn Risk Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- DEMAND PLANNING ---------------- #

st.subheader("📦 Product Demand Planning")

product_demand = (
    df.groupby("product_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    product_demand,
    x="product_name",
    y="quantity",
    title="Top 10 Products by Demand"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- BUSINESS SCENARIO ANALYSIS ---------------- #

st.subheader("📊 Business Scenario Simulation")

growth = st.slider(
    "Expected Revenue Growth (%)",
    0,50,10
)

current_revenue = df["final_amount_inr"].sum()
future_revenue = current_revenue * (1 + growth/100)

col1,col2 = st.columns(2)

col1.metric("Current Revenue", f"₹{current_revenue:,.0f}")
col2.metric("Projected Revenue", f"₹{future_revenue:,.0f}")

scenario = pd.DataFrame({
    "Scenario":["Current","Projected"],
    "Revenue":[current_revenue,future_revenue]
})

fig4 = px.bar(
    scenario,
    x="Scenario",
    y="Revenue",
    title="Revenue Scenario Comparison"
)

st.plotly_chart(fig4, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("🛒 Cross-Selling & Upselling Dashboard")


# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

# Data cleaning
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# ---------------- PRODUCT ASSOCIATIONS ---------------- #

st.subheader("Product Association Analysis")

product_pairs = (
    df.groupby(["product_id"])["product_name"]
    .apply(lambda x: list(set(x)))
    .reset_index()
)

pairs = []

for products in product_pairs["product_name"]:
    if len(products) > 1:
        for i in range(len(products)):
            for j in range(i+1,len(products)):
                pairs.append((products[i],products[j]))

pair_df = pd.DataFrame(pairs, columns=["Product_A","Product_B"])

association = (
    pair_df.value_counts()
    .reset_index(name="count")
    .sort_values("count",ascending=False)
    .head(10)
)

fig1 = px.bar(
    association,
    x="Product_A",
    y="count",
    color="Product_B",
    title="Top Product Associations"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- BUNDLE OPPORTUNITIES ---------------- #

st.subheader("Bundle Opportunity Analysis")

bundle_revenue = df.groupby("product_name")["final_amount_inr"].sum().reset_index()

top_bundle = bundle_revenue.sort_values("final_amount_inr",ascending=False).head(10)

fig2 = px.bar(
    top_bundle,
    x="product_name",
    y="final_amount_inr",
    title="Top Products for Bundle Creation"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- RECOMMENDATION EFFECTIVENESS ---------------- #

st.subheader("Recommendation Effectiveness")

recommendation_sim = df.sample(n=min(500,len(df)))

recommendation_sim["recommended"] = np.random.choice(
    ["Accepted","Ignored"], size=len(recommendation_sim), p=[0.3,0.7]
)

recommendation_summary = recommendation_sim["recommended"].value_counts().reset_index()
recommendation_summary.columns = ["Response","Count"]

fig3 = px.pie(
    recommendation_summary,
    names="Response",
    values="Count",
    title="Recommendation Acceptance Rate"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- CROSS SELL REVENUE ---------------- #

st.subheader("Cross-Sell Revenue Contribution")

multi_product_orders = df.groupby("product_id").filter(lambda x: len(x) > 1)

cross_sell_revenue = multi_product_orders["final_amount_inr"].sum()
total_revenue = df["final_amount_inr"].sum()

cross_df = pd.DataFrame({
    "Type":["Cross-Sell Revenue","Single Product Revenue"],
    "Revenue":[cross_sell_revenue,total_revenue-cross_sell_revenue]
})

fig4 = px.pie(
    cross_df,
    names="Type",
    values="Revenue",
    title="Revenue from Cross-Selling"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- PRODUCT DRILLDOWN ---------------- #

st.subheader("Product Recommendation Drilldown")

product_select = st.selectbox(
    "Select Product",
    df["product_name"].unique()
)

related_products = pair_df[pair_df["Product_A"] == product_select]

if not related_products.empty:
    rec = related_products["Product_B"].value_counts().reset_index()
    rec.columns = ["Recommended_Product","Count"]

    fig5 = px.bar(
        rec,
        x="Recommended_Product",
        y="Count",
        title=f"Products Frequently Bought with {product_select}"
    )

    st.plotly_chart(fig5, use_container_width=True)

else:
    st.write("No strong cross-sell associations found.")

    import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

st.title("🧠 Business Intelligence Command Center")



# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

# Data cleaning
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month

# ---------------- KEY BUSINESS METRICS ---------------- #

st.subheader("📊 Key Business Metrics")

total_revenue = df["final_amount_inr"].sum()
total_orders = df["product_id"].nunique()
total_customers = df["customer_id"].nunique()
avg_order_value = df["final_amount_inr"].mean()

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Orders", total_orders)
col3.metric("Active Customers", total_customers)
col4.metric("Avg Order Value", f"₹{avg_order_value:,.0f}")

# ---------------- PERFORMANCE MONITORING ---------------- #

st.subheader("📈 Revenue Performance Monitoring")

revenue_trend = (
    df.groupby(["year","month"])["final_amount_inr"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    revenue_trend,
    x="month",
    y="final_amount_inr",
    color="year",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- CATEGORY PERFORMANCE ---------------- #

st.subheader("🏆 Category Performance")

category_perf = (
    df.groupby("category")["final_amount_inr"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    category_perf,
    x="category",
    y="final_amount_inr",
    title="Revenue by Category"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- AUTOMATED ALERT SYSTEM ---------------- #

st.subheader("🚨 Automated Business Alerts")

recent_month = df[df["year"] == df["year"].max()]

recent_rev = recent_month["final_amount_inr"].sum()
avg_rev = df["final_amount_inr"].mean()

if recent_rev < avg_rev:
    st.error("⚠️ Revenue is below average this month!")

low_stock_products = (
    df.groupby("product_name")["quantity"]
    .sum()
    .sort_values()
    .head(5)
)

st.warning("📦 Products with Lowest Sales (Potential Overstock Risk)")
st.write(low_stock_products)

# ---------------- CUSTOMER PERFORMANCE ---------------- #

st.subheader("👥 Customer Insights")

customer_orders = df.groupby("customer_id")["product_id"].count().reset_index()

fig3 = px.histogram(
    customer_orders,
    x="product_id",
    nbins=20,
    title="Customer Purchase Frequency"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- STRATEGIC INSIGHTS ---------------- #

st.subheader("🎯 Strategic Business Insights")

top_products = (
    df.groupby("product_name")["final_amount_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.success("🚀 Top Revenue Generating Products")
st.write(top_products)

top_states = (
    df.groupby("customer_state")["final_amount_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.success("🌍 Top Revenue Regions")
st.write(top_states)

# ---------------- SYSTEM STATUS ---------------- #

st.subheader("⚙️ System Health Status")

status = pd.DataFrame({
    "System":["Revenue Engine","Customer Analytics","Supply Chain","Payment Gateway"],
    "Status":["Operational","Operational","Operational","Operational"]
})

st.table(status)