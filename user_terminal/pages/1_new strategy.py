import streamlit as st

@st.experimental_dialog("bot logic")
def logic(name):
    st.write(f"select the frequency and logic for {name}")
    reason = st.text_input("Because...")
    if st.button("add"):
        st.rerun()

st.title("Create a new trading strategy here")
name=st.text_input("enter bot name here")
if st.button("impliment"):
    logic(name)





