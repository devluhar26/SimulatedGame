import numpy as np
import pandas as pd
import streamlit as st
st.set_page_config(layout='wide')

row1col1,row1col2 = st.columns([2,3])
row2col1,row2col2 = st.columns([2,3])

with row1col1:
    tile11 = row1col1.container(height=600)
    tile11.title("11 view stock")
    chart_data = pd.DataFrame(np.random.randn(20, 1), columns=["a"])
    tile11.line_chart(chart_data,height=590, use_container_width=True)


with row1col2:
    tile12 = row1col2.container(height=600)
    tile12.title("12 view strategy")
    tab1, tab2, tab3 = tile12.tabs(["strategy", "new", "edit"])

    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

with row2col1:
    tile21 = row2col1.container(height=600)
    tile21.title("21 add macro event")

with row2col2:
    tile22 = row2col2.container(height=600)
    tile22.title("22 view active orders")
    tab1, tab2 = tile22.tabs(["active orders", "past orders"])

    with tab1:
        df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))

        st.dataframe(df,use_container_width=True)

    with tab2:
        df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))

        st.dataframe(df,use_container_width=True)