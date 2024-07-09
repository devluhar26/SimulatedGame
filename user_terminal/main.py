import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None




def login():

    st.header("Log in")
    roley = st.text_input("enter username")

    if st.button("Log in"):
        st.session_state.role = roley
        st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()


role = st.session_state.role

logout_page = st.Page(logout, title="Log out")

request_1 = st.Page(
    "page/1_overview.py",
    title="overview",
    default=True,

)
request_2 = st.Page(
    "page/2_new.py", title="New"
)


account_pages = [logout_page]
request_pages = [request_1, request_2]

st.title("Welcome "+st.session_state.role)

if st.session_state.role != None:
    pg = st.navigation({"Account": account_pages} | {"Tools": [request_1, request_2]})
else:
    pg = st.navigation([st.Page(login)])

pg.run()