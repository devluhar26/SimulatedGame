import streamlit as st
import pandas as pd
import numpy as np
import random
from code_editor import code_editor
import json

@st.experimental_dialog("Create a new trading strategy")
def logic(name):
    st.write(f"set the trading logic for {name}")
    ##add bot logic widgets here
    if st.button("add"):
        st.rerun()


st.title("Create a new trading strategy here")
name = st.text_input("enter bot name here")
###
with open('resources/example_custom_buttons_bar_adj.json') as json_button_file_alt:
    custom_buttons_alt = json.load(json_button_file_alt)

with open('resources/example_custom_buttons_set.json') as json_button_file:
    custom_buttons = json.load(json_button_file)

with open('resources/example_info_bar.json') as json_info_file:
    info_bar = json.load(json_info_file)

height = [19, 22]
language = "python"
theme = "default"
shortcuts = "vscode"
focus = False
btns = custom_buttons_alt
ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}

response_dict = code_editor("demo_sample_python_code", height=height, lang=language, theme=theme, shortcuts=shortcuts,
                            focus=focus, buttons=btns, info=info_bar, props=ace_props)

if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
    st.write("Response type: ", response_dict['type'])
    st.code(response_dict['text'], language=response_dict['lang'])
#####
if st.button("impliment"):
    pass
    #logic(name)

# else:
#     f"{st.session_state.logic['name']} has now been added (this is when the strat are added to sql)"
#     if st.button("ok"):
#         st.write(st.session_state)
#         st.rerun()
