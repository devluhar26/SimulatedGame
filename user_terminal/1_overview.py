import os
import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
import random
from code_editor import code_editor
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
st.write(st.session_state.user)
user_db_path = os.path.join(BASE_DIR, st.session_state.user + ".db")
connect_user = sqlite3.connect(user_db_path)
curs_user = connect_user.cursor()

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

#
tab1, tab2, tab3 = st.tabs(["overview", "strategies", "modify strategy"])

with tab1:


    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    st.line_chart(chart_data)
    st.write("add portfolio value here")


with tab2:
    st.title("simulated trading game")
    st.write("need to import table [docs.streamlit.io](https://docs.streamlit.io/).")


    curs_user.execute("SELECT * FROM strategy")
    data = {
        'strategy name': [row[0] for row in curs_user.fetchall()],
    }
    ##change the array in line 14 for the strategies true performance

    df = pd.DataFrame(data)
    event = st.dataframe(
        df,
        on_select='rerun',
        selection_mode='multi-row',
        use_container_width=True,height=400
    )

    st.button("modify")
    st.button("delete", type="primary")
with tab3:
    option = st.selectbox(
        "Select the strategy you wish to modify",
        data["strategy name"])
    with open('user_terminal/page/resources/example_custom_buttons_bar_adj.json') as json_button_file_alt:
        custom_buttons_alt = json.load(json_button_file_alt)

    with open('user_terminal/page/resources/example_info_bar.json') as json_info_file:
        info_bar = json.load(json_info_file)

    height = [20, 10]
    btns = custom_buttons_alt
    st.write("Adjust the strategy below then Hit Save")

    response_dict = code_editor("####strategy file path#####", height=height, buttons=btns, info=info_bar)
    if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
        code = response_dict['text']


    st.write(" #### add the trading logic widgets below####")
#
