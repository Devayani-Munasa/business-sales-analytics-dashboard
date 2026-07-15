import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Business Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Database Connection
# -----------------------------
connection = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="Hrithik.11@",
    database="sales_dashboard"
)

# -----------------------------
# Load Data
# -----------------------------
query = "SELECT * FROM sales;"
df = pd.read_sql(query, connection)

connection.close()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filter Data")
st.sidebar.markdown("---")
st.sidebar.info("Use the filters below to explore the sales data.")

years = sorted(df["order_year"].unique())
selected_year = st.sidebar.selectbox(
    "Select Year",
    options=["All"] + list(years)
)

regions = sorted(df["region"].unique())
selected_region = st.sidebar.selectbox(
    "Select Region",
    options=["All"] + regions
)

categories = sorted(df["category"].unique())
selected_category = st.sidebar.selectbox(
    "Select Category",
    options=["All"] + categories
)

filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["order_year"] == selected_year
    ]

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == selected_category
    ]

# -----------------------------
# Dashboard
# -----------------------------
st.title("📊 Business Sales Analytics Dashboard")
st.markdown(
    "Analyze sales performance with interactive charts and filters."
)

st.success("Connected to MySQL Successfully! ✅")

# KPI Calculations
total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
total_orders = filtered_df["order_id"].nunique()
total_quantity = filtered_df["quantity"].sum()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("📦 Total Orders", total_orders)
col4.metric("🛒 Quantity Sold", total_quantity)

st.caption(f"Showing **{len(filtered_df)}** records")
from datetime import datetime

st.caption(
    f"Last Updated: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}"
)

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Sales by Category")
    st.plotly_chart(fig, width="stretch")

category_sales = (
     filtered_df.groupby("category")["sales"]
      .sum()
      .reset_index()
)

fig = px.bar(
    category_sales,
    x="category",
    y="sales",
    text_auto=".2s",
    title="Total Sales by Category"
)
fig.update_layout(
    xaxis_title=None,
    yaxis_title=None
)
st.plotly_chart(fig, width="stretch")

# -----------------------------
# Sales by Region
# -----------------------------
with col_right:
    st.subheader("🌍 Sales by Region")
    st.plotly_chart(fig_region, width="stretch")

region_sales = (
     filtered_df.groupby("region")["sales"]
      .sum()
      .reset_index()
)

fig_region = px.pie(
    region_sales,
    names="region",
    values="sales",
    title="Sales Distribution by Region",
    hole=0.4
)
fig_region.update_layout(
    xaxis_title=None,
    yaxis_title=None
)
st.plotly_chart(fig_region, width="stretch")

# -----------------------------
# Monthly Sales Trend
# -----------------------------
st.subheader("📅 Monthly Sales Trend")

month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

monthly_sales = (
     filtered_df.groupby("order_month")["sales"]
      .sum()
      .reindex(month_order)
      .reset_index()
)

fig_month = px.line(
    monthly_sales,
    x="order_month",
    y="sales",
    markers=True,
    title="Monthly Sales Trend"
)
fig_month.update_layout(
    xaxis_title=None,
    yaxis_title=None
)

st.plotly_chart(fig_month, width="stretch")
# -----------------------------
# Top 10 Customers
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Customers")
    st.plotly_chart(fig_customers, width="stretch")


top_customers = (
    filtered_df.groupby("customer_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_customers = px.bar(
    top_customers,
    x="sales",
    y="customer_name",
    orientation="h",
    text_auto=".2s",
    title="Top 10 Customers by Sales"
)

fig_customers.update_layout(
    xaxis_title=None,
    yaxis_title=None
)

fig_customers.update_layout(yaxis={'categoryorder':'total ascending'})

st.plotly_chart(fig_customers, width="stretch")
# -----------------------------
# Top 10 Products
# -----------------------------
with col2:
    st.subheader("📦 Top 10 Products")
    st.plotly_chart(fig_products, width="stretch")

top_products = (
    filtered_df.groupby("product_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x="sales",
    y="product_name",
    orientation="h",
    text_auto=".2s",
    title="Top 10 Products by Sales"
)

fig_products.update_layout(yaxis={'categoryorder':'total ascending'})

fig_products.update_layout(
    xaxis_title=None,
    yaxis_title=None
)

st.plotly_chart(fig_products, width="stretch")

# -----------------------------
# Profit by Category
# -----------------------------
st.subheader("📈 Profit by Category")

profit_category = (
    filtered_df.groupby("category")["profit"]
    .sum()
    .reset_index()
)

fig_profit = px.bar(
    profit_category,
    x="category",
    y="profit",
    text_auto=".2s",
    title="Profit by Category"
)

fig_profit.update_layout(
    xaxis_title=None,
    yaxis_title=None
)

st.plotly_chart(fig_profit, width="stretch")

st.subheader("📋 Sales Data")

st.dataframe(filtered_df, width="stretch", height=400)