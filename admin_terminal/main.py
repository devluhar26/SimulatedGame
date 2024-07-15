import streamlit as st

st.set_page_config(layout='wide')

row1 = st.columns(3)
row2 = st.columns(3)

for col in row1 + row2:
    tile = col.container(height=400)
    tile.title(":balloon:")