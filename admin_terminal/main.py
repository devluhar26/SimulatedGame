import streamlit as st
from streamlit_elements import elements, mui, html

st.set_page_config(layout='wide')

with elements("new_element"):

    mui.Typography("Hello world")

