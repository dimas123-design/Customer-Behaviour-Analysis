import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Layout
st.set_page_config(page_title="Customer Behavior Analysis", layout="wide")

# Load data
@st.cache_data
def load_data():
    sale = pd.read_csv('/home/tegaryans/Downloads/customer_data.csv')
    return sale

sale = load_data()

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Overview", "Visualization", "Segmentation", "Insights & Recommendations"])

# Overview
if page == "Overview":
    st.title("📊 Customer Behavior Overview")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", sale["id"].nunique())
    col2.metric("Average Income", f"{sale['income'].mean():,.2f}")
    col3.metric("Total Product Categories", sale["product_category"].nunique())
    
    st.subheader("Sample Data")
    st.dataframe(sale.head())

# Customer Behavior Visualization
elif page == "Visualization":
    st.title("📈 Customer Behavior Visualization")

    # Age Distribution
    st.subheader("Customer Age Distribution")
    fig, ax = plt.subplots(figsize=(10, 3))
    sns.histplot(sale["age"], bins=10, kde=True, ax=ax)
    ax.set_title("Customer Age Distribution")
    st.pyplot(fig)

    # Most Popular Product Categories
    st.subheader("Top Product Categories by Number of Transactions")
    top_categories = sale["product_category"].value_counts().head(10)
    st.bar_chart(top_categories)

    # Additional Analysis: Total Revenue per Product Category
    st.subheader("Top Product Categories by Total Revenue")
    revenue_per_category = sale.groupby("product_category")["purchase_amount"].sum().sort_values(ascending=False).head(10)
    st.bar_chart(revenue_per_category)    

    # Customer Loyalty Status
    st.subheader("Customer Loyalty Status")
    loyalty_counts = sale["loyalty_status"].value_counts()
    st.bar_chart(loyalty_counts)

# Customer Segmentation
elif page == "Segmentation":
    st.title("👥 Customer Segmentation")

    segment = sale.groupby("loyalty_status")["id"].nunique()
    st.bar_chart(segment)
    
    st.write("""
    - **Gold Customers**: The most active customers who shop frequently.
    - **Silver Customers**: Customers with moderate transaction activity.
    - **Regular Customers**: Customers who shop less frequently.
    """)

    # Additional Analysis: Average Transactions per Customer in Each Loyalty Category
    st.subheader("Average Transactions per Customer by Loyalty Category")
    transaction_per_customer = sale.groupby("loyalty_status")["purchase_amount"].mean()
    st.bar_chart(transaction_per_customer)
    
    st.write("""
    - If "Regular Customers" have a low average transaction value, it means they are large in number but shop infrequently.
    - "Gold Customers" may be fewer, but if their average transaction value is high, they shop more often and contribute significantly to revenue.
    """)

# Insights & Recommendations
elif page == "Insights & Recommendations":
    st.title("💡 Insights & Recommendations")

    st.markdown("""
    **Findings:**
    - Most customers are between 25-35 years old.
    - The "Clothing" category has the highest number of transactions.
    - However, the category with the highest total revenue may be different (e.g., "Electronics").
    - Most customers fall into the "Regular" category.
    - The average transaction per customer is lower for "Regular Customers" compared to "Gold Customers".

    **Recommendations:**
    - Make loyalty programs more attractive to encourage "Regular" customers to upgrade to "Silver" or "Gold".
    - Increase promotions for less popular product categories.
    - Focus on **high-revenue product categories**, not just those with the most transactions.
    - Further analyze customers with **low purchase frequency** to improve retention.
    """)
