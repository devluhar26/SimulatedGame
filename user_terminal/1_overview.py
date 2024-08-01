import os
import sqlite3
import time

import streamlit as st
import pandas as pd
import numpy as np
import random
from code_editor import code_editor
import json
from github import Github
from streamlit_autorefresh import st_autorefresh

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ex_path = os.path.join(BASE_DIR,"exchange.db")
connect_exchange = sqlite3.connect( ex_path )
curs_exchange = connect_exchange.cursor()


user_db_path = os.path.join(BASE_DIR,st.session_state.user +"/"+st.session_state.user + ".db")
connect_user = sqlite3.connect(user_db_path,check_same_thread=False)
curs_user = connect_user.cursor()

stock_db_path = os.path.join(BASE_DIR, "stock_prices.db")
conn_stock = sqlite3.connect(stock_db_path,check_same_thread=False)
curs_stock = conn_stock.cursor()
html_style_string = '''<style>
@media (min-width: 576px)
section div.block-container {
  padding-left: 20rem;
}
section div.block-container {
  padding-left: 4rem;
  padding-right: 4rem;
  max-width: 80rem;
}  

</style>'''
st.markdown(html_style_string, unsafe_allow_html=True)
st_autorefresh()
def tuple_to_array_str(tuple):
    array = []
    for data in tuple:
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append(str(x))
        array.append(temp)  # 3D array
    return array

#
tab1, tab2, tab3 = st.tabs(["overview", "strategies", "modify strategy"])
with tab1:
    name = [row[0] for row in curs_stock.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    stock = st.selectbox("Select which stock you would like to use the strategy on", name)

    # row0=[row[0] for row in curs_stock.execute(f"SELECT bid FROM [{stock}]").fetchall()]
    # row1=[row[0] for row in curs_stock.execute(f"SELECT ask FROM [{stock}]").fetchall()]
    row2 = [row[0] for row in curs_stock.execute(f"SELECT last_trade_price FROM [{stock}]").fetchall()]
    row3 = [row[0] for row in curs_stock.execute(f"SELECT time FROM [{stock}]").fetchall()]
    # "bid": row0,"ask":row1,
    data = {"last trade price": row2, "time": row3}
    try:
        chart_data = pd.DataFrame(data)
        chart_data.set_index('time', inplace=True)
        st.line_chart(chart_data, use_container_width=True)
    except:
        st.warning("Loading....")
    col1, col2 = st.columns([2, 2])
    tile4 = st.container(height=490)
    tile4.title("Current portfolio")
    data = {
        'stock': [row[0] for row in curs_user.execute("SELECT * FROM portfolio").fetchall()],
        'quantity': [row[1] for row in curs_user.execute("SELECT * FROM portfolio").fetchall()],
        'initial price per share': [row[2] for row in curs_user.execute("SELECT * FROM portfolio").fetchall()],
        'long/short': [row[3] for row in curs_user.execute("SELECT * FROM portfolio").fetchall()],

    }
    ##change the array in line 14 for the strategies true performance

    df = pd.DataFrame(data)
    event = tile4.dataframe(df, hide_index=True, use_container_width=True)

    with col1:
        tile1 = col1.container(height=520)
        tile1.title("view my current orders")
        df = pd.DataFrame(curs_exchange.execute("SELECT order_number,stock,buy_or_sell,ask_bid_price_per_share,quantity,time_of_execution FROM active_orders WHERE (username)=(?)",(st.session_state.user,)).fetchall()).sort_values(5,ascending=False)
        tile1.dataframe(df, use_container_width=True,hide_index=True)
    with col2:
        tile2 = col2.container(height=520)
        tile2.title("view my past orders ")
        past=[]
        st.write()
        for x in tuple_to_array_str(curs_exchange.execute("SELECT reciept_number,stock,bid_pps,quantity,time_of_execution FROM past_orders WHERE (buyer_username)=(?)",(st.session_state.user,)).fetchall()):
            past.append(x)

        for x in tuple_to_array_str(curs_exchange.execute("SELECT reciept_number,stock,ask_pps,quantity,time_of_execution FROM past_orders WHERE (seller_username)=(?)",(st.session_state.user,)).fetchall()):
            past.append(x)
        df = pd.DataFrame(past).sort_values(4,ascending=False)
        tile2.dataframe(df, use_container_width=True,hide_index=True )

with tab2:
    st.title("Currently active strategies")



    data = {
        'strategy name': [row[0] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'location': [row[1] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'stock': [row[2] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'take profit': [row[3] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'stop loss': [row[4] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'minimum trade size': [row[5] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'maximum trade size': [row[6] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'minimum trade duration': [row[7] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'maximum duration': [row[8] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'trade frequency': [row[9] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
    }
    ##change the array in line 14 for the strategies true performance

    df = pd.DataFrame(data)
    event = st.dataframe(
        df,
        on_select='rerun',
        selection_mode='multi-row',
         hide_index = True,
        use_container_width=True

    )
    st.write(event.selection["rows"])

    if st.button("modify"):
        pass
    if st.button("delete", type="primary"):

        for x in range(len(event.selection["rows"])):
            st.write(event.selection["rows"][x])
            curs_user.execute("DELETE FROM  strategy WHERE (strategy_name)=(?)",([row[0] for row in curs_user.execute("SELECT * FROM strategy").fetchall()][event.selection["rows"][x]],))
            connect_user.commit()
            st.error("strategy has been removed")
            time.sleep(1)
            #st.rerun()
with tab3:
    option = st.selectbox(
        "Select the strategy you wish to modify",
        data["strategy name"])

    with open('user_terminal/resources/example_custom_buttons_bar_adj.json') as json_button_file_alt:
        custom_buttons_alt = json.load(json_button_file_alt)

    with open('user_terminal/resources/example_info_bar.json') as json_info_file:
        info_bar = json.load(json_info_file)

    height = [20, 10]
    btns = custom_buttons_alt
    st.write("Adjust the strategy below then Hit Save")
    try:
        startcode=open(str(curs_user.execute("SELECT strategy_location FROM strategy WHERE strategy_name=?", (option,)).fetchone()[0]),"r").read()
    except:
        startcode=""
    response_dict = code_editor(startcode, height=height, buttons=btns, info=info_bar)
    if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
        code = response_dict['text']
        st.write(" #### add the trading logic widgets below####")

        stock = st.selectbox("Select which stock you would like to use the strategy on",[row[0] for row in curs_stock.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()])
        option_2 = st.selectbox(
            "some question about stop loss and take profit?",
            ("none","stop loss","take profit","both"))
        stop_loss=None
        take_profit=None
        if option_2=="none":
            pass
        if option_2=="stop loss":
            stop_loss = st.slider("select stop loss and take profit using the slider", 0.0, 100.0, 25.0)
        if option_2=="take profit":
            take_profit = st.slider("select stop loss and take profit using the slider", 0.0, 100.0, 75.0)
        if option_2=="both":
            size = st.slider("select stop loss and take profit using the slider", 0.0, 100.0, (25.0, 75.0))
            stop_loss=size[0]
            take_profit=size[1]


        size_option = st.selectbox(
            "some question about min and max trade size?",
            ("none","min size","max size","both"))
        min_size=None
        max_size=None
        if size_option=="none":
            pass
        if size_option=="min size":
            min_size = st.slider("select min size", 0.0, 100.0, 25.0)
        if size_option=="max size":
            max_size = st.slider("select max size trade", 0.0, 100.0, 75.0)
        if size_option=="both":
            trade_size = st.slider("select min and max trade size", 0.0, 100.0, (25.0, 75.0))
            min_size=trade_size[0]
            max_size=trade_size[1]

        timeframe_option = st.selectbox(
            "some question about min and max timeframe?",
            ("none", "min timeframe", "max timeframe", "both"))
        min_timeframe = None
        max_timeframe = None
        if timeframe_option == "none":
            pass
        if timeframe_option == "min timeframe":
            min_timeframe = st.slider("select min timeframe", 0.0, 60.0, 20.0)
        if timeframe_option == "max timeframe":
            max_timeframe = st.slider("select  max timeframe", 0.0, 60.0, 40.0)
        if timeframe_option == "both":
            trade_timeframe = st.slider("select min and max timeframe", 0.0, 60.0, (20.0, 40.0))
            min_timeframe = trade_timeframe[0]
            max_timeframe = trade_timeframe[1]
        trades_per_hour = st.number_input("select how many trades you would like to do per hour. If you would like to do less then 1 trade per hour, use decimals ")
        if st.button("add"):
            file=open("user_terminal/"+st.session_state.user+"/"+ option + ".py","w")
            file.write(code)
            curs_user.execute("UPDATE strategy SET (stock, take_profit,stop_loss,min_size,max_size,min_timeframe,max_timeframe,trade_frequency) = (?,?,?,?,?,?,?,?) WHERE (strategy_name)=(?)",(stock,take_profit,stop_loss,min_size,max_size,min_timeframe,max_timeframe,trades_per_hour,option))
            connect_user.commit()
            st.success("the strategy has been modified",icon="✅")
            st.rerun()



