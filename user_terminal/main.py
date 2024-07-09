import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Requester"]


def login():

    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES)

    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()


role = st.session_state.role

logout_page = st.Page(logout, title="Log out")

request_1 = st.Page(
    "page/1_overview.py",
    title="overview",
    default=(role == "Requester"),

)
request_2 = st.Page(
    "page/2_new.py", title="title"
)


account_pages = [logout_page]
request_pages = [request_1, request_2]

st.title("Request manager")

page_dict = {}
if st.session_state.role in ["Requester"]:
    page_dict["Request"] = request_pages


if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()