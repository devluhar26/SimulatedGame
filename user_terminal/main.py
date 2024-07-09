import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Requester", "Admin"]


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
settings = st.Page("settings.py", title="Settings")
request_1 = st.Page(
    "pages/1_overview.py",
    title="overview",
    default=(role == "Requester"),
)
request_2 = st.Page(
    "pages/2_new.py", title="title"
)

admin_1 = st.Page(
    "admin_terminal/main.py",
    title="Admin 1",

    default=(role == "Admin"),
)

account_pages = [logout_page, settings]
request_pages = [request_1, request_2]
admin_pages = [admin_1]

st.title("Request manager")

page_dict = {}
if st.session_state.role in ["Requester", "Admin"]:
    page_dict["Request"] = request_pages

if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()