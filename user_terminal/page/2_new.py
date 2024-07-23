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

st.markdown(html_style_string, unsafe_allow_html=True)
st.write(st.session_state.user)
if "bot_name" not in st.session_state:
    st.session_state.bot_name = None
@st.experimental_dialog("Create a new trading strategy")
def logic(name,code):
    st.write(f"set the trading logic for {name}")
    values = st.slider(
        "Select a range of values",
        0.0, 100.0, (25.0, 75.0))
    number = st.number_input("Insert a number")
    option = st.selectbox(
        "How would you like to be contacted?",
        ("Email", "Home phone", "Mobile phone"))
    local_path = "user_terminal/"+ st.session_state.user + ".db"



    ##add bot logic widgets here
    if st.button("add"):
        repo.create_file("user_terminal/"+ st.session_state.bot_name + ".py", "it works", code, branch="main", )
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        user_db_path = os.path.join(BASE_DIR,  st.session_state.user + ".db")
        connect_user = sqlite3.connect(user_db_path)
        curs_user = connect_user.cursor()
        #curs_user.execute("")
        #INSERT INTO STATEMENT^
        connect_user.commit()
        file = open(user_db_path, "rb")
        repo.update_file(local_path, ".", file.read(), repo.get_contents(local_path).sha, "main")
        st.rerun()


st.title("Create a new trading strategy here")
st.session_state.bot_name = st.text_input("enter bot name here")
###

with open('user_terminal/page/resources/example_custom_buttons_bar_adj.json') as json_button_file_alt:
    custom_buttons_alt = json.load(json_button_file_alt)

with open('user_terminal/page/resources/example_info_bar.json') as json_info_file:
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