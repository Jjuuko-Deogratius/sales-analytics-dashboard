import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Heading Section

st.title("📊 Sales Analytics Dashboard")

st.caption(
    "Retail Sales Business Intelligence Dashboard "
    "for monitoring sales performance."
)

@st.cache_data
def load_data():

    df = pd.read_csv("data/cleaned_sales_data.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    return df


df = load_data()

# Now create a Branch filter:

branch_options = sorted(df["Branch"].unique())
category_options = sorted(df["Category"].unique())
product_options = sorted(df["Product"].unique())
payment_options = sorted(df["Payment_Method"].unique())
customer_options = sorted(df["Customer_Type"].unique())

st.sidebar.header("Filters")
selected_branches = st.sidebar.multiselect(
    "Branch",
    options=branch_options,
    default=branch_options
)

# Add a category filter
selected_categories = st.sidebar.multiselect(
    "Category",
    options=category_options,
    default=category_options
)

# Add advanced filters
# Instead of filling the entire sidebar with controls, we'll put some inside an expander:

with st.sidebar.expander("More Filters"):

    selected_products = st.multiselect(
        "Product",
        options=product_options,
        default=product_options
    )

    selected_customer_types = st.multiselect(
        "Customer Type",
        options=customer_options,
        default=customer_options
    )

    selected_payment_methods = st.multiselect(
        "Payment Method",
        options=payment_options,
        default=payment_options
    )

# Add date filters
minimum_date = df["Date"].min().date()
maximum_date = df["Date"].max().date()

start_date = st.sidebar.date_input(
    "Start Date",
    value=minimum_date,
    min_value=minimum_date,
    max_value=maximum_date
)

end_date = st.sidebar.date_input(
    "End Date",
    value=maximum_date,
    min_value=minimum_date,
    max_value=maximum_date
)

# Now add an important validation check:
if start_date > end_date:

    st.sidebar.error(
        "Start Date cannot be after End Date."
    )

    st.stop()

# Apply the filters
filtered_df = df[
    (df["Branch"].isin(selected_branches)) &
    (df["Category"].isin(selected_categories)) &
    (df["Product"].isin(selected_products)) &
    (df["Customer_Type"].isin(selected_customer_types)) &
    (df["Payment_Method"].isin(selected_payment_methods)) &
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
].copy()


# Show users what they're currently viewing
st.caption(
    f"Showing {len(filtered_df):,} transactions "
    f"from {start_date:%d %b %Y} "
    f"to {end_date:%d %b %Y}."
)

# Create the four KPI calculations

total_revenue = filtered_df["Total_Sales"].sum()

total_transactions = filtered_df["Transaction_ID"].nunique()

total_units = filtered_df["Quantity"].sum()

if total_transactions > 0:
    average_transaction_value = (
        total_revenue / total_transactions
    )
else:
    average_transaction_value = 0

# KPI section heading
st.subheader("Key Performance Indicators")

# Create KPI cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"UGX {total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "Transactions",
        f"{total_transactions:,}"
    )

with col3:
    st.metric(
        "Units Sold",
        f"{total_units:,}"
    )

with col4:
    st.metric(
        "Average Transaction",
        f"UGX {average_transaction_value:,.0f}"
    )

st.divider()

# Tabs
overview_tab, products_tab, customer_tab, data_tab = st.tabs(
    [
        "📈 Overview",
        "📦 Products",
        "👥 Customers & Payments",
        "🗃️ Data"
    ]
)

# Building the Overview tab
with overview_tab:
    # Monthly Revenue
        monthly_revenue = (
        filtered_df.groupby("Year_Month")["Total_Sales"]
        .sum()
        .reset_index()
    )
        monthly_fig = px.line(
    monthly_revenue,
    x="Year_Month",
    y="Total_Sales",
    markers=True,
    title="Monthly Revenue Trend",
    labels={
        "Year_Month": "Month",
        "Total_Sales": "Revenue (UGX)"
    }
)
        st.plotly_chart(
        monthly_fig,
        width="stretch"
    )
        # Branch and Category charts
        branch_revenue = (
        filtered_df.groupby("Branch")["Total_Sales"]
        .sum()
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )

        category_revenue = (
        filtered_df.groupby("Category")["Total_Sales"]
        .sum()
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )

        branch_fig = px.bar(
        branch_revenue,
        x="Branch",
        y="Total_Sales",
        title="Revenue by Branch",
        labels={
            "Total_Sales": "Revenue (UGX)"
        }
    )

        category_fig = px.bar(
        category_revenue,
        x="Category",
        y="Total_Sales",
        title="Revenue by Category",
        labels={
            "Total_Sales": "Revenue (UGX)"
        }
    )
        left, right = st.columns(2)

        with left:
            st.plotly_chart(
                branch_fig,
                width="stretch"
        )

        with right:
            st.plotly_chart(
                category_fig,
                width="stretch"
        )
        st.caption(
        "Note: The final month contains partial-month data."
    )    


# Building the Products tab
with products_tab:
    # Top products by revenue

    product_revenue = (
        filtered_df.groupby("Product")["Total_Sales"]
        .sum()
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
        .head(10)
    )
    product_revenue = product_revenue.sort_values(
        "Total_Sales"
    )
    product_revenue_fig = px.bar(
        product_revenue,
        x="Total_Sales",
        y="Product",
        orientation="h",
        title="Top 10 Products by Revenue",
        labels={
            "Total_Sales": "Revenue (UGX)"
        }
    )
    # Top products by units sold
    product_units = (
        filtered_df.groupby("Product")["Quantity"]
        .sum()
        .reset_index()
        .sort_values("Quantity", ascending=False)
        .head(10)
    )

    product_units = product_units.sort_values(
        "Quantity"
    )

    product_units_fig = px.bar(
        product_units,
        x="Quantity",
        y="Product",
        orientation="h",
        title="Top 10 Products by Units Sold",
        labels={
            "Quantity": "Units Sold"
        }
    )
    # Now putting them side by side:
    left, right = st.columns(2)

    with left:
        st.plotly_chart(
            product_revenue_fig,
            width="stretch"
        )

    with right:
        st.plotly_chart(
            product_units_fig,
            width="stretch"
        )

    # product performance table
    product_summary = (
        filtered_df
        .groupby(["Product", "Category"])
        .agg(
            Revenue=("Total_Sales", "sum"),
            Units_Sold=("Quantity", "sum"),
            Transactions=("Transaction_ID", "nunique")
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )
    # Displaying It
    st.subheader("Product Performance")

    st.dataframe(
        product_summary,
        width="stretch",
        hide_index=True
    )

# Building the Customers & Payments tabs
with customer_tab:
    # analysing customer type
    customer_revenue = (
        filtered_df
        .groupby("Customer_Type")["Total_Sales"]
        .sum()
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )
    customer_fig = px.bar(
        customer_revenue,
        x="Customer_Type",
        y="Total_Sales",
        title="Revenue by Customer Type",
        labels={
            "Customer_Type": "Customer Type",
            "Total_Sales": "Revenue (UGX)"
        }
    )
    # Payment method analysis
    payment_revenue = (
        filtered_df
        .groupby("Payment_Method")["Total_Sales"]
        .sum()
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )
    payment_fig = px.bar(
        payment_revenue,
        x="Payment_Method",
        y="Total_Sales",
        title="Revenue by Payment Method",
        labels={
            "Payment_Method": "Payment Method",
            "Total_Sales": "Revenue (UGX)"
        }
    )

    left, right = st.columns(2)

    with left:
        st.plotly_chart(
            customer_fig,
            width="stretch"
        )

    with right:
        st.plotly_chart(
            payment_fig,
            width="stretch"
        )

# Build the Data tab
with data_tab:

    st.subheader("Filtered Transaction Data")

    # Choosing most useful columns
    display_columns = [
        "Transaction_ID",
        "Date",
        "Branch",
        "Product",
        "Category",
        "Quantity",
        "Unit_Price",
        "Total_Sales",
        "Payment_Method",
        "Customer_Type"
    ]
    st.dataframe(
        filtered_df[display_columns],
        width="stretch",
        hide_index=True
    )

    # Adding a CSV download
    csv_data = filtered_df[
        display_columns
    ].to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Data",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv",
        width="stretch"
    )

# footer
st.divider()

st.caption(
    "Sales Analytics Dashboard | "
    "Built with Python, Pandas, Plotly and Streamlit"
)

# Handle empty filter results
# There is one problem we should solve.

# Suppose someone:
# removes every branch or removes every category
# Then our filtered dataset contains no records.

if filtered_df.empty:
    st.warning(
        "No sales records match the selected filters."
    )
    st.stop()