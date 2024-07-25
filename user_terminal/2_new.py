import os.path
import sqlite3

import streamlit_authenticator as stauth

import streamlit as st
import pandas as pd
import numpy as np
import random
from code_editor import code_editor
import json
from github import Github
g=Github("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")
repo=g.get_repo("Blackelm-Systematic/SimulatedGame")




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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

user_db_path = os.path.join(BASE_DIR, st.session_state.user + ".db")
connect_user = sqlite3.connect(user_db_path)
curs_user = connect_user.cursor()

stock_db_path = os.path.join(BASE_DIR, "stock_prices.db")
conn_stock = sqlite3.connect(stock_db_path)
curs_stock = conn_stock.cursor()

st.markdown(html_style_string, unsafe_allow_html=True)
if "bot_name" not in st.session_state:
    st.session_state.bot_name = None

@st.experimental_dialog("Create a new trading strategy",width="large")
def logic(name,code):
    st.write(f"set the trading logic for {name}")
    stock = st.selectbox("Select which stock you would like to use the strategy on",[row[0] for row in curs_stock.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()])
    option = st.selectbox(
        "some question about stop loss and take profit?",
        ("none","stop loss","take profit","both"))
    stop_loss=None
    take_profit=None
    if option=="none":
        pass
    if option=="stop loss":
        stop_loss = st.slider("select stop loss and take profit using the slider", 0.0, 100.0, 25.0)
    if option=="take profit":
        take_profit = st.slider("select stop loss and take profit using the slider", 0.0, 100.0, 75.0)
    if option=="both":
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
    local_path = "user_terminal/"+ st.session_state.user + ".db"
    if st.button("add"):
        repo.create_file("user_terminal/"+ st.session_state.bot_name + ".py", "it works", code, branch="main", )
        curs_user.execute("INSERT INTO strategy(strategy_name, strategy_location,stock, take_profit,stop_loss,min_size,max_size,min_timeframe,max_timeframe,trade_frequency) VALUES (?,?,?,?,?,?,?,?,?,?)",(st.session_state.bot_name,"user_terminal/"+ st.session_state.bot_name + ".py",stock,take_profit,stop_loss,min_size,max_size,min_timeframe,max_timeframe,trades_per_hour))
        connect_user.commit()
        file = open(user_db_path, "rb")
        repo.update_file(local_path, ".", file.read(), repo.get_contents(local_path).sha, "main")
        st.rerun()
        st.switch_page("user_terminal/1_overview.py")



st.title("Create a new trading strategy here")
st.session_state.bot_name = st.text_input("enter bot name here")
###

with open('user_terminal/resources/example_custom_buttons_bar_adj.json') as json_button_file_alt:
    custom_buttons_alt = json.load(json_button_file_alt)

with open('user_terminal/resources/example_info_bar.json') as json_info_file:
    info_bar = json.load(json_info_file)

height = [20, 22]
btns = custom_buttons_alt
st.write("Program your strategy below then Hit Save")



response_dict = code_editor("", height=height,   buttons=btns, info=info_bar)
if response_dict['type'] == "submit" and len(response_dict['text']) != 0 and len(st.session_state.bot_name) != 0:
    code=response_dict['text']
    logic(st.session_state.bot_name,code)
elif  response_dict['type'] == "submit" and len(response_dict['text']) == 0:
    st.warning('Add your strategy before Hitting Save', icon="⚠️")

#####