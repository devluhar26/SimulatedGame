import sqlite3

import streamlit as st
st.set_page_config(layout='wide')

if "user" not in st.session_state:
    st.session_state.user = None
import os.path
def open_SQL():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "credentials.db")
    connect_credentials= sqlite3.connect(db_path)
    curs_credentials = connect_credentials.cursor()
# used to store all the usernames and passwords as a 2d array
credentials = []
def retrieve_credentials():             #STATIC METHOD
    open_SQL.curs_credentials.execute( "SELECT * FROM Credentials" )
    for data in open_SQL.curs_credentials.fetchall():
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( x )
        open_SQL.credentials.append( temp )  #3D array

def add_credentials(username,password):

    open_SQL.curs_credentials.execute("INSERT INTO  Credentials (username,password) VALUES (?,?)",
                             (username,password))
    open_SQL.connect_credentials.commit()
    open_SQL.connect_credentials.close()
    retrieve_credentials()
    st.write(open_SQL.credentials)
    st.success("you have registered")
def checker(username,password):
    retrieve_credentials()
    temp=[str(username),str(password)]
    ##add some more errors ie no input and try registering
    if temp in open_SQL.credentials:
        st.session_state.user = username
        st.rerun()
    else:
        st.warning("Invalid Credentials")
def login():

    st.header("Log in")
    username = st.text_input("enter username")
    password = st.text_input("enter password")
    col1, col2 = st.columns([1, 1])  # Adjust column ratios as needed

    with col1:
        if st.button("Log in",use_container_width=True):
            checker(username, password)

    with col2:
        if st.button("Register", use_container_width=True):
            retrieve_credentials()
            if username in [row[0] for row in open_SQL.credentials]:
                st.warning("this username already exist, try a different one")
                return
            if username == "" or password == "":
                st.warning("one or more of the fields are blank, please add some text")
            else:
                add_credentials(username,password)


        ##add a login checking system here

def logout():
    st.session_state.user = None
    st.rerun()

def main():
    logout_page = st.Page(logout, title="Log out")
    request_1 = st.Page(
        "page/1_overview.py",
        title="overview",
        default=True,

    )
    request_2 = st.Page(
        "page/2_new.py", title="New"
    )

    st.title("Blackelm")

    if st.session_state.user != None:
        pg = st.navigation({"Account": [logout_page]} | {"Tools": [request_1, request_2]})
    else:
        pg = st.navigation([st.Page(login)])

    pg.run()
if __name__=="__main__":
    main()