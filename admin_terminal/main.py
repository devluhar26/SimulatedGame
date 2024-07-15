import streamlit as st
row1col1,row1col2 = st.columns(2)
row2col1,row2col2 = st.columns(2)

with row1col1:
    tile11 = row1col1.container(height=120)
    tile11.title("11")
with row1col2:
    tile12 = row1col2.container(height=120)
    tile12.title("12")
with row2col1:
    tile21 = row2col1.container(height=120)
    tile21.title("21")
with row2col2:
    tile22 = row2col2.container(height=120)
    tile22.title("22")