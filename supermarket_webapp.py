import pandas as pd
import plotly.express as px
import streamlit as st
import openpyxl 

st.set_page_config(page_title= 'Sales Dashboard',
                   page_icon=':bar_chart:', 
                   layout='wide'
)

df = pd.read_excel(
        io= "supermarket.xlsx",
        engine= 'openpyxl',
        nrows=1000,
        
)
df['DateTime'] = df["Date"] + ' ' + df["Time"]
df['DateTime'] = pd.to_datetime(df['DateTime'])
df['Hour'] = df["DateTime"].dt.hour

# sidebar
st.sidebar.header('Filtering; ')

city = st.sidebar.multiselect(
    "Select the City",
    options=df["City"].sort_values().unique(),
    default=df["City"].unique()
)

branch = st.sidebar.multiselect(
    "Select the Branch",
    options=df["Branch"].sort_values().unique(),
    default=df["Branch"].unique()
)

gender =  st.sidebar.multiselect(
    "Select the Gender",
    options=df["Gender"].sort_values().unique(),
    default=df["Gender"].unique()
)
cust_type = st.sidebar.multiselect(
    "Customer Type",
    options=df["Customer_type"].sort_values().unique(),
    default=df["Customer_type"].unique()
)
dfselect = df.query(
    "City == @city & Customer_type == @cust_type & Branch == @branch & Gender == @gender "
)


st.title(":bar_chart: SUPERMARKET SALES DASHBOARD")
st.markdown("##")

total_sales = int(dfselect['Total'].sum())
average_rating = round(dfselect["Rating"].mean(), 1)
starrating = ":star:" * int(round(average_rating, 0 ))
average_sale_transaction = round(dfselect["Total"].mean(), 2)

left_col , mid_col , right_col = st.columns(3)
with left_col:
    st.subheader("Total Sales: ")
    st.subheader(f"US $ {total_sales:,}")
    
with mid_col:
    st.subheader("Average Rating: ")
    st.subheader(f"{average_rating} {starrating}")
with right_col:
    st.subheader("Average Sale Transaction: ")
    st.subheader(f"US $ {average_sale_transaction}")
    
st.markdown("-----")

product_sales = (
    dfselect.groupby("Product line").sum()[["Total"]].sort_values(by='Total')
)


fig_product_sales = px.bar(
    product_sales,
    y="Total",
    x=product_sales.index,
   
    title='<b>Total Product Sales per Product<b>',
    color_discrete_sequence=["#0083B8"] * len(product_sales),
    template="plotly_white",
    )
    
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
    xaxis=dict(tickmode="linear"),
)

hour_sales = (
    dfselect.groupby("Hour").sum()[["Quantity"]].sort_values(by="Quantity")
)

product_sales_per_hour = px.bar(
    hour_sales,
    y="Quantity",
    x=hour_sales.index,
    title='<b>Product Most Sales per Hour<b>',
    template="plotly_white",
    color_discrete_sequence=["#0083B8"] * len(hour_sales),
)
product_sales_per_hour.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
    xaxis=dict(tickmode="linear"),
)

left_col , right_col = st.columns(2)
left_col.plotly_chart(fig_product_sales , use_container_width=True)

right_col.plotly_chart(product_sales_per_hour, use_container_width=True)