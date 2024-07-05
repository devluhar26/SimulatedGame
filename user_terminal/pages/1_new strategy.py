import streamlit as st

@st.experimental_dialog("Cast your vote")
def logic(name):
    st.write(f"set the trading logic for {name}")
    ##add bot logic widgets here
    if st.button("add"):
        st.session_state.logic = {"name": name,}
        st.rerun()

if "logic" not in st.session_state:
    st.title("Create a new trading strategy here")
    name = st.text_input("enter bot name here")
    if st.button("impliment"):
        logic(name)

else:
    f"{st.session_state.logic['name']} has now been added"

