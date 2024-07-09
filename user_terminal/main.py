import sqlite3

import streamlit as st

if "user" not in st.session_state:
    st.session_state.user = None

connect_credentials = sqlite3.connect( "credentials.db" )

curs_credentials = connect_credentials.cursor()
# used to store all the usernames and passwords as a 2d array
credentials = []
def retrieve_credentials():             #STATIC METHOD
    curs_credentials.execute("SELECT name FROM sqlite_master WHERE type='table'")
    st.write( curs_credentials.fetchall())
    curs_credentials.execute( "SELECT username,password FROM Credentials" )
    for data in curs_credentials.fetchall():
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( x )
        credentials.append( temp )  #3D array



def checker(username,password):
    retrieve_credentials()
    temp=[str(username),str(password)]
    st.write(credentials)
    if temp in credentials:
        st.session_state.user = username
        st.rerun()

def login():

    st.header("Log in")
    username = st.text_input("enter username")
    password = st.text_input("enter password")

    if st.button("Log in"):
        checker(username,password)
        ##add a login checking system here

def logout():
    st.session_state.user = None
    st.rerun()


role = st.session_state.user

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

st.title("Welcome "+str(st.session_state.user))

if st.session_state.user != None:
    pg = st.navigation({"Account": account_pages} | {"Tools": [request_1, request_2]})
else:
    pg = st.navigation([st.Page(login)])

pg.run()