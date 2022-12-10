'''Displays premade graphs on a webpage

Receives:
.csv dataframes

Returns:
Graphs on streamlit
'''

# Imports
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from functions import filter_dataframe
from pathlib import Path
from functions import s3_csv_downloader
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Bikes forever store",
    page_icon="🚲",
    layout="wide",
)
#set up containers to work in
lines = st.container()
scatterplot = st.container()
bar = st.container()

path_csv = Path(__file__).parent.parent.parent/'outputs'

if path_csv.exists():
    file_names = []
    list_csv = []

    for i in path_csv.iterdir():
        # Save keys of dictionary that contain file name into list
        file_names.append(i.name)

        if i.name == "transactions.csv":
            chart_data = pd.read_csv(i)

        if i.name == "products.csv":
            chart_data_products = pd.read_csv(i)

    # Graph out line chart
    with lines:
        st.markdown("# 📉 Transactions per month")
        st.markdown(">Shows the trend of transactions in the year")
        # Add month column
        chart_data['transaction_date'] = pd.to_datetime(chart_data["transaction_date"])
        chart_data['month'] = chart_data["transaction_date"].dt.month
        # Dataframe grouping by month
        df_transactions_per_month = chart_data.groupby("month").size().reset_index()
        df_transactions_per_month.columns = ["month", "transaction_count"]
        df_transactions_per_month = df_transactions_per_month[df_transactions_per_month["transaction_count"] > 1500]

        fig = px.line(df_transactions_per_month, x="month", y="transaction_count", title='Transactions per month',markers=True)
        st.plotly_chart(fig, use_container_width=True)

    #Graph out scatterplot chart
    with scatterplot:
        st.write("# 📈 Order list price vs Order standard cost")
        st.markdown(">Describes the correlation between the order list price and the order standard cost")
        fig = px.scatter(chart_data, x="list_price", y="standard_cost", trendline="ols")
        st.plotly_chart(fig, use_container_width=True)

    #Graph out bar chart
    with bar:
        st.write("# 📈 Order list price vs Order standard cost")
        st.markdown(">How many products per brand and product_line are there?")
        fig = px.bar(chart_data_products, y=["brand","product_line"], color="product_line", barmode="group")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Folder outputs with datasets not exists please shoot the button, wait a minute and reload the page")
    button = st.button("Create Output folder with csv files")
    if button:
        st.experimental_singleton.clear()
        s3_csv_downloader()

st.text('Fuente: https://www.kaggle.com/datasets/archit9406/customer-transaction-dataset')
