import streamlit as st
st.set_page_config(layout='wide')

row1col1,row1col2 = st.columns([2,3])
row2col1,row2col2 = st.columns([2,3])

with row1col1:
    tile11 = row1col1.container(height=400)
    tile11.title("11")
    tab1, tab2, tab3 = tile11.tabs(["Cat", "Dog", "Owl"])

    with tab1:
        tile11.header("A cat")
        tile11.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    with tab2:
        tile11.header("A dog")
        tile11.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        tile11.header("An owl")
        tile11.image("https://static.streamlit.io/examples/owl.jpg", width=200)


with row1col2:
    tile12 = row1col2.container(height=400)
    tile12.title("12")
with row2col1:
    tile21 = row2col1.container(height=400)
    tile21.title("21")
with row2col2:
    tile22 = row2col2.container(height=400)
    tile22.title("22")