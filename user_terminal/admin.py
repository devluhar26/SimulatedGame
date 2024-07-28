import sqlite3

import numpy as np
import pandas as pd
import streamlit as st
import read_stock_price
print(read_stock_price.get_stock_names())
st.set_page_config(layout='wide')
connect_stock = sqlite3.connect("stock_prices.db")
curs_stock = connect_stock.cursor()
stock="AAPL"
print()

connect_exchange = sqlite3.connect( "exchange.db" )
curs_exchange = connect_exchange.cursor()
row1col1,row1col2 = st.columns([2,3])
row2col1,row2col2 = st.columns([2,3])
def tuple_to_array(tuple):
    array=[]
    for data in  tuple:
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( x )
        array.append( temp )  #3D array
    return array
with row1col1:
    tile11 = row1col1.container(height=600)
    tile11.title("11 view stock")
    try:
        stock = tile11.selectbox("Select which stock you would like to use the strategy on",[row[0] for row in curs_stock.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()])
    except:
        stock="AAPL"
    chart_data = pd.DataFrame(tuple_to_array(curs_stock.execute(f"SELECT * FROM ",(stock,)).fetchall()), columns=["bid","ask","last trade price","time"],)
    tile11.line_chart(chart_data,height=590, use_container_width=True)


with row1col2:
    tile12 = row1col2.container(height=600)
    tile12.title("12 view strategy")
    tab1, tab2, tab3 = tile12.tabs(["strategy", "new", "edit"])

    with tab1:
        df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))

        st.dataframe(df, use_container_width=True)

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

with row2col1:
    tile21 = row2col1.container(height=600)
    tile21.title("21 add macro event")

with row2col2:
    tile22 = row2col2.container(height=600)
    tile22.title("22 view active orders")
    tab1, tab2 = tile22.tabs(["active orders", "past orders"])

    with tab1:
        df = pd.DataFrame(curs_exchange.execute("SELECT * FROM active_orders").fetchall())

        st.dataframe(df,use_container_width=True, hide_index=True)

    with tab2:
        df = pd.DataFrame(curs_exchange.execute("SELECT * FROM past_orders").fetchall())

        st.dataframe(df,use_container_width=True, hide_index=True)