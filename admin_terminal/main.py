import streamlit as st

st.set_page_config(layout='wide')

row1 = st.columns(3)
row2 = st.columns(3)
tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

for col in row1 + row2:
    tile = col.container(height=400)
    tile.title(":balloon:")

    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)