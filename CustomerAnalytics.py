import streamlit as st
import pandas as pd
import plotly.express as px

st.title("👥 Customer Segmentation Dashboard")


# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")

# ---------------- RFM ANALYSIS ---------------- #


snapshot_date = df["order_date"].max()

rfm = df.groupby("customer_id").agg({
    "order_date": lambda x: (snapshot_date - x.max()).days,
    "product_id": "count",
    "final_amount_inr": "sum"
}).reset_index()

rfm.columns = ["customer_id", "Recency", "Frequency", "Monetary"]

# RFM Scores
rfm["R_score"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1])
rfm["F_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1,2,3,4])
rfm["M_score"] = pd.qcut(rfm["Monetary"], 4, labels=[1,2,3,4])

rfm["RFM_segment"] = rfm["R_score"].astype(str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str)

# ---------------- CUSTOMER SEGMENTS ---------------- #

def segment_customer(row):
    if row["R_score"] == 4 and row["F_score"] >= 3:
        return "Loyal Customers"
    elif row["R_score"] == 4:
        return

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🧭 Customer Journey Analytics Dashboard")


# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")



# ---------------- PURCHASE PATTERNS ---------------- #

st.subheader("Purchase Frequency Distribution")

purchase_freq = df.groupby("customer_id")["product_id"].nunique().reset_index()

fig2 = px.histogram(
    purchase_freq,
    x="product_id",
    title="Purchase Frequency Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- CUSTOMER LIFETIME VALUE ---------------- #

st.subheader("Customer Lifetime Value (CLV) Distribution")

clv = df.groupby("customer_id")["final_amount_inr"].sum().reset_index()

fig3 = px.histogram(
    clv,
    x="final_amount_inr",                                                                   
    title="Customer Lifetime Value Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("👑 Prime Membership Analytics Dashboard")


# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")

# If Prime column does not exist, simulate example
if "prime_member" not in df.columns:
    df["prime_member"] = df["customer_id"].apply(
    lambda x: "Prime" if int(x.split("_")[-1]) % 2 == 0 else "Non-Prime"
)
# ---------------- PRIME VS NON PRIME REVENUE ---------------- #

st.subheader("Prime vs Non-Prime Revenue Contribution")

prime_rev = df.groupby("prime_member")["final_amount_inr"].sum().reset_index()

fig1 = px.pie(
    prime_rev,
    names="prime_member",
    values="final_amount_inr",
    title="Revenue Contribution by Membership Type"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- PURCHASE BEHAVIOR ---------------- #

st.subheader("Average Order Value Comparison")

aov = df.groupby("prime_member")["final_amount_inr"].mean().reset_index()

fig2 = px.bar(
    aov,
    x="prime_member",
    y="final_amount_inr",
    title="Average Order Value (Prime vs Non-Prime)"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- PURCHASE FREQUENCY ---------------- #

st.subheader("Purchase Frequency")

purchase_freq = df.groupby(["prime_member","customer_id"])["product_id"].count().reset_index()

freq_summary = purchase_freq.groupby("prime_member")["product_id"].mean().reset_index()

fig3 = px.bar(
    freq_summary,
    x="prime_member",
    y="product_id",
    title="Average Orders per Customer"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- RETENTION ANALYSIS ---------------- #

st.subheader("Customer Retention")

repeat_customers = df.groupby(["prime_member","customer_id"])["product_id"].count().reset_index()

repeat_customers["repeat"] = repeat_customers["product_id"].apply(lambda x: "Repeat" if x > 1 else "One-Time")

retention = repeat_customers.groupby(["prime_member","repeat"]).size().reset_index(name="count")

fig4 = px.bar(
    retention,
    x="prime_member",
    y="count",
    color="repeat",
    barmode="group",
    title="Customer Retention Comparison"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- PRIME BUSINESS INSIGHTS ---------------- #

st.subheader("Prime Category Preferences")

prime_data = df[df["prime_member"]=="Prime"]

category_pref = prime_data.groupby("category")["final_amount_inr"].sum().reset_index()

fig5 = px.bar(
    category_pref.sort_values("final_amount_inr",ascending=False),
    x="category",
    y="final_amount_inr",
    title="Top Categories for Prime Customers"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------- CUSTOMER PROFILE DRILLDOWN ---------------- #

st.subheader("Customer Profile Drill-down")

customer_select = st.selectbox(
    "Select Customer",
    df["customer_id"].unique()
)

customer_data = df[df["customer_id"] == customer_select]

st.write("Membership Type:", customer_data["prime_member"].iloc[0])

st.write("Total Orders:", customer_data["product_id"].count())

st.write("Total Spend:", customer_data["final_amount_inr"].sum())

st.write(customer_data[["order_date","category","final_amount_inr"]])

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("👥 Demographics & Behavior Dashboard")


# Load dataset
df = pd.read_csv("amazon_allyearclean.csv")

df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")
df["final_amount_inr"] = pd.to_numeric(df["final_amount_inr"], errors="coerce")

# ---------------- SIMULATE AGE DATA (if not available) ---------------- #

if "age" not in df.columns:
    np.random.seed(42)
    df["age"] = np.random.randint(18, 60, len(df))

# Create age groups
bins = [18,25,35,45,60]
labels = ["18-25","26-35","36-45","46-60"]
df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)


# ---------------- AGE GROUP ANALYSIS ---------------- #    
st.subheader("Revenue by Age Group")
age_rev = df.groupby("age_group")["final_amount_inr"].sum().reset_index()

fig1 = px.bar(
    age_rev,
    x="age_group",
    y="final_amount_inr",
    title="Revenue Contribution by Age Group"
)

st.plotly_chart(fig1, use_container_width=True)