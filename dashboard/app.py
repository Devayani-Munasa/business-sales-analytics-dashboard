import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
from datetime import datetime
from dotenv import load_dotenv
import os

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="Business Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------
# Load Environment Variables
# ---------------------------------
load_dotenv()

# ---------------------------------
# Load Data
# ---------------------------------
@st.cache_data
def load_data():

    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        query = "SELECT * FROM sales"

        df = pd.read_sql(query, connection)

        connection.close()

        return df

    except Exception as e:
        st.error("❌ Unable to connect to MySQL Database")
        st.error(e)
        st.stop()


df = load_data()
# ---------------------------------
# Helper Functions
# ---------------------------------

def format_number(value):
    """Format numbers for KPI cards."""

    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    elif value >= 1_000:
        return f"${value / 1_000:.2f}K"

    else:
        return f"${value:,.2f}"


# ---------------------------------
# Sales by Category Chart
# ---------------------------------

def create_category_chart(data):

    category_sales = (
        data.groupby("category")["sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category_sales,
        x="category",
        y="sales",
        title="📊 Sales by Category",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Sales"
    )

    return fig


# ---------------------------------
# Sales by Region Chart
# ---------------------------------

def create_region_chart(data):

    region_sales = (
        data.groupby("region")["sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_sales,
        names="region",
        values="sales",
        hole=0.45,
        title="🌍 Sales by Region"
    )

    return fig

    # ---------------------------------
# Monthly Sales Trend Chart
# ---------------------------------

def create_monthly_chart(data):

    month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    monthly_sales = (
        data.groupby("order_month")["sales"]
        .sum()
        .reindex(month_order)
        .reset_index()
    )

    fig = px.line(
        monthly_sales,
        x="order_month",
        y="sales",
        markers=True,
        title="📅 Monthly Sales Trend"
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Sales"
    )

    return fig


# ---------------------------------
# Top Customers Chart
# ---------------------------------

def create_customers_chart(data):

    top_customers = (
        data.groupby("customer_name")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_customers,
        x="sales",
        y="customer_name",
        orientation="h",
        text_auto=".2s",
        title="🏆 Top 10 Customers"
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Sales",
        yaxis_title=None
    )

    return fig


# ---------------------------------
# Top Products Chart
# ---------------------------------

def create_products_chart(data):

    top_products = (
        data.groupby("product_name")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_products,
        x="sales",
        y="product_name",
        orientation="h",
        text_auto=".2s",
        title="📦 Top 10 Products"
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Sales",
        yaxis_title=None
    )

    return fig


# ---------------------------------
# Profit by Category Chart
# ---------------------------------

def create_profit_chart(data):

    profit_category = (
        data.groupby("category")["profit"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        profit_category,
        x="category",
        y="profit",
        text_auto=".2s",
        title="📈 Profit by Category"
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Profit"
    )

    return fig
    # ---------------------------------
# Sidebar Filters
# ---------------------------------
st.sidebar.title("📌 Dashboard Filters")

st.sidebar.markdown("""
Welcome to the **Business Sales Analytics Dashboard**.

Use the filters below to explore your sales data interactively.
""")

st.sidebar.info("""
### Available Filters

📅 Year

🌍 Region

📦 Category
""")

st.sidebar.divider()

# Year Filter
years = ["All"] + sorted(df["order_year"].unique().tolist())

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)

# Region Filter
regions = ["All"] + sorted(df["region"].unique().tolist())

selected_region = st.sidebar.selectbox(
    "Select Region",
    regions
)

# Category Filter
categories = ["All"] + sorted(df["category"].unique().tolist())

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

st.sidebar.divider()

st.sidebar.success("📊 Dataset Overview")

st.sidebar.write(f"**Total Records:** {len(df):,}")
st.sidebar.write(f"**Years:** {df['order_year'].nunique()}")
st.sidebar.write(f"**Regions:** {df['region'].nunique()}")
st.sidebar.write(f"**Categories:** {df['category'].nunique()}")

# ---------------------------------
# Apply Filters
# ---------------------------------
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
    # ---------------------------------
# Dashboard Header
# ---------------------------------
st.title("📊 Business Sales Analytics Dashboard")

st.markdown("""
Welcome to the **Business Sales Analytics Dashboard**.

This dashboard helps analyze sales performance using interactive charts,
filters, and key business metrics powered by **Python, MySQL, Pandas,
Plotly, and Streamlit**.
""")

st.success("🟢 Connected to MySQL Database")

# ---------------------------------
# KPI Calculations
# ---------------------------------
total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
total_orders = filtered_df["order_id"].nunique()
total_quantity = filtered_df["quantity"].sum()

# ---------------------------------
# KPI Cards
# ---------------------------------
st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Sales",
        format_number(total_sales)
    )

with col2:
    st.metric(
        "📈 Total Profit",
        format_number(total_profit)
    )

with col3:
    st.metric(
        "📦 Total Orders",
        total_orders
    )

with col4:
    st.metric(
        "🛒 Quantity Sold",
        f"{total_quantity:,}"
    )

# ---------------------------------
# Dashboard Information
# ---------------------------------
st.caption(f"📄 Showing {len(filtered_df):,} records")

st.caption(
    f"🕒 Last Updated: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}"
)
# ---------------------------------
# Create Charts
# ---------------------------------
fig_category = create_category_chart(filtered_df)
fig_region = create_region_chart(filtered_df)
fig_month = create_monthly_chart(filtered_df)
fig_customers = create_customers_chart(filtered_df)
fig_products = create_products_chart(filtered_df)
fig_profit = create_profit_chart(filtered_df)

# ---------------------------------
# Dashboard Visualizations
# ---------------------------------

# Row 1
st.divider()

left, right = st.columns(2)

with left:
    st.subheader("📊 Sales by Category")
    st.plotly_chart(fig_category, width="stretch")

with right:
    st.subheader("🌍 Sales by Region")
    st.plotly_chart(fig_region, width="stretch")

# Row 2
st.divider()

st.subheader("📅 Monthly Sales Trend")
st.plotly_chart(fig_month, width="stretch")

# Row 3
st.divider()

left, right = st.columns(2)

with left:
    st.subheader("🏆 Top 10 Customers")
    st.plotly_chart(fig_customers, width="stretch")

with right:
    st.subheader("📦 Top 10 Products")
    st.plotly_chart(fig_products, width="stretch")

# Row 4
st.divider()

st.subheader("📈 Profit by Category")
st.plotly_chart(fig_profit, width="stretch")
# ---------------------------------
# Sales Data
# ---------------------------------
st.divider()

st.subheader("📋 Sales Data")

st.dataframe(
    filtered_df,
    width="stretch",
    height=400
)

# ---------------------------------
# Download Filtered Data
# ---------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# ---------------------------------
# Business Insights
# ---------------------------------
st.divider()

st.subheader("💡 Business Insights")

best_region = (
    filtered_df.groupby("region")["sales"]
    .sum()
    .idxmax()
)

best_category = (
    filtered_df.groupby("category")["sales"]
    .sum()
    .idxmax()
)

best_customer = (
    filtered_df.groupby("customer_name")["sales"]
    .sum()
    .idxmax()
)

best_month = (
    filtered_df.groupby("order_month")["sales"]
    .sum()
    .idxmax()
)

col1, col2 = st.columns(2)

with col1:
    st.success(f"🌍 Best Performing Region: **{best_region}**")
    st.success(f"📦 Best Selling Category: **{best_category}**")

with col2:
    st.success(f"🏆 Top Customer: **{best_customer}**")
    st.success(f"📅 Highest Sales Month: **{best_month}**")