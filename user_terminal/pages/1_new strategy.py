import streamlit as st

@st.experimental_dialog("bot logic")
def logic(name):
    st.write(f"select the frequency and logic for {name}")
    ## add widgets to set logic and frequency here
    if st.button("add"):
        st.rerun()
if "logic" not in st.session_state:

    st.title("Create a new trading strategy here")
    name=st.text_input("enter bot name here")
    if st.button("impliment"):
        logic(name)

else:
    f"{st.session_state.logic['name']} has been added"


