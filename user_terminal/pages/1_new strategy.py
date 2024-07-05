import streamlit as st

@st.experimental_dialog("Cast your vote")
def vote():
    st.write(f"Why is your favorite?")
    if st.button("Submit"):
        pass
if __name__ == "__main__":
    vote()




