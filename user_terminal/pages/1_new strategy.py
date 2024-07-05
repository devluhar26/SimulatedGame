import streamlit as st

@st.experimental_dialog("Cast your vote")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()

if "vote" not in st.session_state:
    st.title("Create a new trading strategy here")
    name = st.text_input("enter bot name here")
    if st.button("impliment"):
        vote(name)

else:
    f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"

