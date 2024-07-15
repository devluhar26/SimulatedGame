import sqlite3
import os.path
from github import Github

import streamlit as st
st.set_page_config(layout='wide')
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Dev's personal access token, need to change it
g=Github("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")
repo=g.get_repo("Blackelm-Systematic/SimulatedGame")
if "user" not in st.session_state:
    st.session_state.user = None
def cur(filename):
    global curs_credentials, connect_credentials ,db_path
    db_path = os.path.join(BASE_DIR,filename+".db")
    connect_credentials = sqlite3.connect(db_path)
    curs_credentials = connect_credentials.cursor()
#SQL
def save_SQL(db_path,filename):
    cur(filename)
    connect_credentials.commit()
    with open(db_path, "rb") as file:
        repo.update_file(r"user_terminal/"+filename+".db", ".", file.read(), repo.get_contents(r"user_terminal/"+filename+".db").sha,
                         "main")
        st.write("saved"+filename)
# used to store all the usernames and passwords as a 2d array
credentials = []
def retrieve_credentials():             #STATIC METHOD
    cur("credentials")
    for data in  curs_credentials.execute("SELECT * from Credentials").fetchall():
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( x )
        credentials.append( temp )  #3D array

def add_credentials(username,password):
    cur("credentials")
    curs_credentials.execute("INSERT INTO  Credentials (Username,Password) VALUES (?,?)",
                             (username, password))
    save_SQL(db_path=db_path,filename="credentials")
    # repo.create_file("user_terminal/"+username+"/"+username+".db", "test message", "", branch="main")
    # cur(username)
    # curs_credentials.execute("CREATE TABLE Credentials (username	TEXT NOT NULL UNIQUE,password	TEXT NOT NULL,PRIMARY KEY(username));")
    # save_SQL(db_path=db_path,filename=username)
    st.success("you have registered")
def checker(username,password):
    retrieve_credentials()
    temp=[str(username),str(password)]
    ##add some more errors ie no input and try registering
    if temp in credentials:
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
            if username in [row[0] for row in credentials]:
                st.warning("this username already exist, try a different one")
                return
            if username == "" or password == "":
                st.warning("one or more of the fields are blank, please add some text")
            else:
                add_credentials(username,password)
                st.rerun()

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