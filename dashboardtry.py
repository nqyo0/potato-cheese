import pandas as pd
import streamlit as st
import plotly.express as px # type: ignore
import os

# Load the CSV from Google Drive using the direct link
url = "https://drive.google.com/uc?id=1X-qnbxHtEQ9kYz6uz34DKd5CyrPD1HZL&export=download"
data = pd.read_csv(url)

# Print the first few rows to verify
print(data.head())

# Title and description
st.title("Geographical Distribution of Customers and Sellers")
st.write("Dashboard created by **Naqiya Fadlilatun Nisa**")
st.write("This interactive dashboard shows the distribution of customers and sellers across different cities and states.")

# Filter data
st.sidebar.header("Filters")
state_filter = st.sidebar.multiselect("Select State(s)", options=data['customer_state'].unique(), default=data['customer_state'].unique())

# Apply filter
filtered_data = data[data['customer_state'].isin(state_filter)]

# Plotting customer distribution
st.subheader("Customer Distribution Map")
customer_fig = px.scatter_geo(
    filtered_data,
    locationmode='USA-states',
    locations='customer_state',
    hover_name='customer_city',
    size_max=15,
    title='Customer Locations'
)
st.plotly_chart(customer_fig)

# Plotting seller distribution
st.subheader("Seller Distribution Map")
seller_fig = px.scatter_geo(
    filtered_data,
    locationmode='USA-states',
    locations='seller_state',
    hover_name='seller_city',
    size_max=15,
    title='Seller Locations'
)
st.plotly_chart(seller_fig)

# Display data
st.subheader("Raw Data")
st.write(filtered_data)
