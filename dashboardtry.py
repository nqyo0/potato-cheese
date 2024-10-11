import pandas as pd
import streamlit as st
import plotly.express as px

# Load the CSV from Google Drive using the direct link
url = "https://drive.google.com/uc?id=1X-qnbxHtEQ9kYz6uz34DKd5CyrPD1HZL&export=download"
data = pd.read_csv(url)

# Streamlit: Display the first few rows of data
st.title("Geographical Distribution of Customers and Sellers")
st.write("Dashboard created by **Naqiya Fadlilatun Nisa**")
st.write("This interactive dashboard shows the distribution of customers and sellers across different cities and states.")

# Display the first few rows of data
st.subheader("Preview of Data")
st.write(data.head())

# Filter by state
st.sidebar.header("Filters")
state_filter = st.sidebar.multiselect("Select State(s)", options=data['customer_state'].unique(), default=data['customer_state'].unique())

# Apply filter
filtered_data = data[data['customer_state'].isin(state_filter)]

# Plotting customer distribution
st.subheader("Customer Distribution Map")
if 'customer_city' in filtered_data.columns and 'customer_state' in filtered_data.columns:
    customer_fig = px.scatter_geo(
        filtered_data,
        locationmode='USA-states',
        locations='customer_state',
        hover_name='customer_city',
        title='Customer Locations'
    )
    st.plotly_chart(customer_fig)
else:
    st.write("The necessary columns for customer location are missing.")

# Plotting seller distribution
st.subheader("Seller Distribution Map")
if 'seller_city' in filtered_data.columns and 'seller_state' in filtered_data.columns:
    seller_fig = px.scatter_geo(
        filtered_data,
        locationmode='USA-states',
        locations='seller_state',
        hover_name='seller_city',
        title='Seller Locations'
    )
    st.plotly_chart(seller_fig)
else:
    st.write("The necessary columns for seller location are missing.")

# Display filtered data
st.subheader("Filtered Data")
st.write(filtered_data)
