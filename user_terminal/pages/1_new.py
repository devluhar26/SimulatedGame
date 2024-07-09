import os.path

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

@st.experimental_dialog("Create a new trading strategy")
def logic(name,code):
    st.write(f"set the trading logic for {name}")
    ##add bot logic widgets here
    if st.button("add"):
        repo.create_file(str(random.randint(0, 5000)) + ".py", "it works", code, branch="main", )
        st.rerun()


st.title("Create a new trading strategy here")
name = st.text_input("enter bot name here")
###

with open('user_terminal/pages/resources/example_custom_buttons_bar_adj.json') as json_button_file_alt:
    custom_buttons_alt = json.load(json_button_file_alt)

with open('user_terminal/pages/resources/example_info_bar.json') as json_info_file:
    info_bar = json.load(json_info_file)

height = [19, 22]
btns = custom_buttons_alt

ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}
response_dict = code_editor("", height=height,   buttons=btns, info=info_bar, props=ace_props)

if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
    st.code(response_dict['text'], language=response_dict['lang'])
    code=response_dict['text']
    st.warning('This is a warning', icon="⚠️")
    if st.button("impliment"):
        logic(name,code)
#####


