import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


order_items = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Ecommerce/order_items_dataset.csv')
orders = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Ecommerce/orders_dataset.csv')
sellers = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Ecommerce/sellers_dataset.csv')
customers = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Ecommerce/customers_dataset.csv')
geolocation = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Ecommerce/geolocation_dataset.csv')
order_payments = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Ecommerce/order_payments_dataset.csv')
order_reviews = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Ecommerce/order_reviews_dataset.csv')
products = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Ecommerce/products_dataset.csv')
product_category = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Ecommerce/product_category_name_translation.csv')

datasets_overview = {
    "customers": customers.head(),
    "geolocation": geolocation.head(),
    "order_items": order_items.head(),
    "order_payments": order_payments.head(),
    "order_reviews": order_reviews.head(),
    "orders": orders.head(),
    "product_category": product_category.head(),
    "products": products.head(),
    "sellers": sellers.head()
}

customer_order = pd.merge( #combine customer and order data into one dataframe
    left= orders,
    right= customers,
    how="left", #take all order data and related customer data
    left_on= "customer_id",
    right_on= "customer_id"
)


merged_item = pd.merge( #merged order item, seller, product, and category
    pd.merge( #table for order_items & sellers
        order_items, sellers,
        how = "left", on='seller_id'
        ),
    pd.merge( #table for  products & category
        products, product_category,
        how = "left",
        on='product_category_name'
        ),
    how="left",
    on="product_id"
    )


all_merged = pd.merge( #merged customer order and merged dataframe item into one
    left=customer_order,
    right=merged_item,
    how="right",
    left_on="order_id",
    right_on="order_id"
)

# Title
st.title("E-Commerce Analytics Dashboard")
st.markdown("## Overview of Sales, Products, and Customer Insights")

# Sidebar
st.sidebar.header("Choose Metrics to View")

# Metric 1: Total Orders
total_orders = len(orders)
st.sidebar.metric(label="Total Orders", value=total_orders)

# Metric 2: Total Revenue
total_revenue = order_items['price'].sum()
st.sidebar.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")

# Metric 3: Total Products Sold
total_products_sold = order_items['order_item_id'].count()
st.sidebar.metric(label="Total Products Sold", value=total_products_sold)

# Sales by Product Category
st.subheader("Sales by Product Category")
product_sales = order_items.merge(products, on='product_id', how='left')
category_sales = product_sales.groupby('product_category_name').price.sum().reset_index()
category_sales = category_sales.merge(product_category, on='product_category_name', how='left')
category_sales = category_sales.rename(columns={'product_category_name_english': 'Category'}).sort_values(by='price', ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='price', y='Category', data=category_sales, palette='viridis', ax=ax)
ax.set_title('Revenue by Product Category', fontsize=14)
ax.set_xlabel('Revenue')
ax.set_ylabel('Category')
st.pyplot(fig)

# Customer Reviews Insights
st.subheader("Customer Satisfaction (Reviews)")
review_scores = order_reviews['review_score'].value_counts().sort_index()

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(x=review_scores.index, y=review_scores.values, palette='coolwarm', ax=ax2)
ax2.set_title('Distribution of Review Scores', fontsize=14)
ax2.set_xlabel('Review Score')
ax2.set_ylabel('Number of Reviews')
st.pyplot(fig2)

# Display Geographical Distribution of Sellers and Customers
st.subheader("Geographical Distribution of Sellers")
sellers_location = sellers['seller_state'].value_counts()

fig3, ax3 = plt.subplots(figsize=(8, 5))
sns.barplot(x=sellers_location.index, y=sellers_location.values, palette='Blues_r', ax=ax3)
ax3.set_title('Number of Sellers by State', fontsize=14)
ax3.set_xlabel('State')
ax3.set_ylabel('Number of Sellers')
st.pyplot(fig3)

st.markdown("### Explore more insights in future updates.")
