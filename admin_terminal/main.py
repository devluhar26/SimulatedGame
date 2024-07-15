import streamlit as st
row1col1,row1col2 = st.columns(2)
row2col1,row2col2 = st.columns(2)

with row1col1:
    st.header("11")

with row1col2:
    st.header("12")

with row2col1:
    st.header("21")

with row2col2:
    st.header("22")
