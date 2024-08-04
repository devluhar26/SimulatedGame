import os
import sqlite3
import matplotlib.pyplot as plt

import altair
import numpy as np
import pandas as pd
import streamlit as st
import read_stock_price
from streamlit_autorefresh import st_autorefresh

st.session_state.user=st.session_state.user

st_autorefresh()
connect_stock = sqlite3.connect("user_terminal/stock_prices.db",check_same_thread=False)
curs_stock = connect_stock.cursor()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_db_path = os.path.join(BASE_DIR, "credentials.db")
connect_credentials = sqlite3.connect(cred_db_path,check_same_thread=False)

curs_credentials = connect_credentials.cursor()

connect_exchange = sqlite3.connect( "user_terminal/exchange.db" ,check_same_thread=False)
curs_exchange = connect_exchange.cursor()
row1col1,row1col2 = st.columns([3,2])
row2col1,row2col2 = st.columns([2,3])
def tuple_to_array(tuple):
    array=[]
    for data in  tuple:
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( x )
        array.append( temp )  #3D array
    return array
def tuple_to_array_str(tuple):
    array=[]
    for data in  tuple:
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( str(x) )
        array.append( temp )  #3D array

    return array
with row1col1:
    tile11 = row1col1.container(height=700)
    tile11.title("11 view stock")
    name=[row[0] for row in curs_stock.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    stock = tile11.selectbox("Select which stock you would like to use the strategy on",name)


    #
    data={"bid": [row[0] for row in curs_stock.execute(f"SELECT * FROM [{stock}]").fetchall()],
          "ask":[row[1] for row in curs_stock.execute(f"SELECT * FROM [{stock}]").fetchall()],
          "last trade price":[row[2] for row in curs_stock.execute(f"SELECT * FROM [{stock}]").fetchall()],
          "time":[row[3] for row in curs_stock.execute(f"SELECT * FROM [{stock}]").fetchall()],}
    try:
        chart_data = pd.DataFrame( data)
        chart_data.set_index('time', inplace=True)
        tile11.line_chart(chart_data, height=570,use_container_width=True)
    except:
        st.warning("Loading....")

with row1col2:
    tile12 = row1col2.container(height=700)
    tile12.title("12 view strategy")

    tile12.write()
    strat=[]
    for user in [row[0] for row in curs_credentials.execute("SELECT username From Credentials").fetchall()]:
        try:
            conn_user=sqlite3.connect("user_terminal/"+user+"/"+user+".db")
            curs_user = conn_user.cursor()
            for x in (tuple_to_array_str(curs_user.execute("SELECT * from strategy").fetchall())):
                x.insert(0,user)
                strat.append(x)
        except:
            pass
    df = pd.DataFrame(strat)
    tile12.dataframe(df, use_container_width=True )

with row2col1:
    tile21 = row2col1.container(height=700)
    tile21.title("21 add macro event")

    table_names = [row[0] for row in
                   curs_stock.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

    # User selects the stock table
    selected_stock = tile21.selectbox("Select which stock you would like to use the strategy on", table_names, key="50")

    # Fetch data for each column
    try:
        bid_prices = [row[3] for row in curs_exchange.execute(
            f"SELECT * FROM active_orders WHERE stock='{selected_stock}' AND buy_or_sell='buy' ORDER BY ask_bid_price_per_share DESC").fetchall()]
        ask_prices = [row[3] for row in curs_exchange.execute(
            f"SELECT * FROM active_orders WHERE stock='{selected_stock}' AND buy_or_sell='sell' ORDER BY ask_bid_price_per_share ASC").fetchall()]
        bid_volumes = [row[4] for row in curs_exchange.execute(
            f"SELECT * FROM active_orders WHERE stock='{selected_stock}' AND buy_or_sell='buy' ORDER BY ask_bid_price_per_share DESC").fetchall()]
        ask_volumes = [row[4] for row in curs_exchange.execute(
            f"SELECT * FROM active_orders WHERE stock='{selected_stock}' AND buy_or_sell='sell' ORDER BY ask_bid_price_per_share ASC").fetchall()]
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")

    # Sorting and preparing the data is now handled by the SQL queries

    # Plotting the data
    fig, ax = plt.subplots()

    # Plot the bid data
    ax.fill_between(bid_prices, bid_volumes, color='green', alpha=0.5, step='post', label='Bid')

    # Plot the ask data
    ax.fill_between(ask_prices, ask_volumes, color='red', alpha=0.5, step='post', label='Ask')

    # Formatting the plot
    ax.set_xlabel('Price')
    ax.set_ylabel('Volume')
    ax.set_title(f'Bid-Ask Spread for {selected_stock}')
    ax.legend()
    ax.grid(True)

    # Display the plot in Streamlit
    tile21.pyplot(fig)
with row2col2:
    tile22 = row2col2.container(height=710)
    tile22.title("22 view active orders")
    tab1, tab2 = tile22.tabs(["active orders", "past orders"])

    with tab1:
        df = pd.DataFrame(curs_exchange.execute("SELECT * FROM active_orders ORDER BY order_number DESC").fetchall())

        st.dataframe(df,use_container_width=True, hide_index=True)

    with tab2:
        df = pd.DataFrame(curs_exchange.execute("SELECT * FROM past_orders ORDER BY reciept_number DESC").fetchall())

        st.dataframe(df,use_container_width=True, hide_index=True)
