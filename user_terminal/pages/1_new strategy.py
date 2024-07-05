import streamlit as st

@st.experimental_dialog("Cast your vote")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.rerun()

if "vote" not in st.session_state:
    if st.button("A"):
        vote("A")
    if st.button("B"):
        vote("B")
