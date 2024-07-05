import streamlit as st

@st.experimental_dialog("Cast your vote")
def logic(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.logic = {"item": item,}
        st.rerun()

if "logic" not in st.session_state:
    st.title("Create a new trading strategy here")
    name = st.text_input("enter bot name here")
    if st.button("impliment"):
        logic(name)

else:
    f"You voted for {st.session_state.logic['item']} because "

