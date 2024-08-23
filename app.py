import snowflake.connector
import streamlit as st
import pandas as pd
import plotly.express as px


def get_snowflake_connection():
    # Establish the connection
    conn = snowflake.connector.connect(
        user='Admin',
        password='',
        account='uc10095.ap-southeast-1',
        warehouse='COMPUTE_WH',
        database='sales_db',
        schema='sales_schema'
        )
    return conn


# Fetch data from Snowflake
@st.cache_data(ttl=600)
def fetch_sales_data():
    conn = get_snowflake_connection()
    query = "SELECT * FROM sales"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit app
st.title('Sales Dashboard')

# Fetch data
sales_data = fetch_sales_data()

# Display data in a table
st.subheader('Sales Data')
st.write(sales_data)

# Filter by date range
st.subheader('Filter by Date Range')

date_range = st.date_input('Select Date Range', [])
print(date_range)
if date_range:
    start_date, end_date = date_range
    print(start_date,end_date)
    filtered_data = sales_data[
        (sales_data['SALE_DATE'] >= start_date) &
        (sales_data['SALE_DATE'] <= end_date)
    ]
    st.write(filtered_data)
else:
    filtered_data = sales_data
    st.write(filtered_data)

# Visualization: Sales Amount Over Time
st.subheader('Sales Amount Over Time')
fig = px.line(filtered_data, x='SALE_DATE', y='SALE_AMOUNT', title='Sales Over Time')
st.plotly_chart(fig)

# Visualization: Sales by Region
st.subheader('Sales by Region')
fig = px.bar(filtered_data, x='REGION_ID', y='SALE_AMOUNT', title='Sales by Region')
st.plotly_chart(fig)

# Visualization: Top Products
st.subheader('Top Products')
fig = px.bar(filtered_data, x='PRODUCT_ID', y='SALE_AMOUNT', title='Top Products')
st.plotly_chart(fig)
