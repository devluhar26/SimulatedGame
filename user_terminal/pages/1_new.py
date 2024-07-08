import streamlit as st
import pandas as pd
import numpy as np
import random
from code_editor import code_editor

@st.experimental_dialog("Create a new trading strategy")
def logic(name):
    st.write(f"set the trading logic for {name}")
    ##add bot logic widgets here
    if st.button("add"):
        st.rerun()


code=""
st.title("Create a new trading strategy here")
name = st.text_input("enter bot name here")
response_dict = code_editor("demo_sample_python_code", height=[19, 22])

if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
    st.write("Response type: ", response_dict['type'])
    st.code(response_dict['text'], language=response_dict['lang'])

if st.button("impliment"):
    pass
    #logic(name)

# else:
#     f"{st.session_state.logic['name']} has now been added (this is when the strat are added to sql)"
#     if st.button("ok"):
#         st.write(st.session_state)
#         st.rerun()
