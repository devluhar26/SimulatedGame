import sqlite3
import os.path
from github import Github

import streamlit as st
from google.cloud.sql.connector import Connector
import pymysql
import sqlalchemy
st.set_page_config(layout='wide')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ="user_terminal/application_default_credentials.json"

# helper function to return SQLAlchemy connection pool
def init_connection_pool(connector: Connector) -> sqlalchemy.engine.Engine:
    # function used to generate database connection
    def getconn() -> pymysql.connections.Connection:
        conn = connector.connect(
            "blackelm-428420:europe-west2:blackelmsimulated",
            "pymysql",
            user="dev",
            password="dev",
            db="blackelm"
        )
        return conn

    # create connection pool
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    return pool

connector=Connector()
pool = init_connection_pool(connector)
db_conn=pool.connect()

g=Github("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")
repo=g.get_repo("Blackelm-Systematic/SimulatedGame")


if "user" not in st.session_state:
    st.session_state.user = None
#SQL


# used to store all the usernames and passwords as a 2d array
credentials = []
def retrieve_credentials():             #STATIC METHOD
    for data in  db_conn.execute(sqlalchemy.text("SELECT * from Credentials")).fetchall():
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( x )
        credentials.append( temp )  #3D array
retrieve_credentials()

def add_credentials(username,password):
    insert_stmt = sqlalchemy.text(
        "INSERT INTO  Credentials (username,password) VALUES (:username,:password)",
    )
    db_conn.execute(insert_stmt, parameters={"username": username, "password": password})
    db_conn.commit()
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