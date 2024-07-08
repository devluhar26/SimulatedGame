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
.floating-side-bar {
    display: flex;
    flex-direction: column;
    position: fixed;
    margin-top: 2rem;
    margin-left: 2.75rem;
    margin-right: 2.75rem;
}
.flt-bar-hd {
    color: #5e6572;
    margin: 1rem 0.1rem 0 0;
}
.floating-side-bar a {
    color: #b3b8c2;

}
.floating-side-bar a:hover {

}
.floating-side-bar a.l2 {

}
</style>'''

st.markdown(html_style_string, unsafe_allow_html=True)

with open('resources/example_custom_buttons_set.json') as json_button_file:
    custom_buttons = json.load(json_button_file)

with open('resources/example_custom_buttons_bar_adj.json') as json_button_file_alt:
    custom_buttons_alt = json.load(json_button_file_alt)

# Load Info bar CSS from JSON file
with open('resources/example_info_bar.json') as json_info_file:
    info_bar = json.load(json_info_file)

# Load Code Editor CSS from file
with open('resources/code_editor.scss') as css_file:
    css_text = css_file.read()


height = [19, 22]
language = "python"
theme = "default"
shortcuts = "vscode"
focus = False
btns = custom_buttons_alt

col1, col2 = st.columns([6, 2])
with col1:
    st.markdown("## Demo")

    # construct props dictionary (->Ace Editor)
    ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}
    response_dict = code_editor("", height=height, lang=language, theme=theme, shortcuts=shortcuts,
                                focus=focus, buttons=btns, info=info_bar, props=ace_props)

    if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
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
