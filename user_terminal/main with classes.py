
import sqlite3
import os.path
from github import Github

import streamlit as st
from google.cloud.sql.connector import Connector
import pymysql
import sqlalchemy
st.set_page_config(layout='wide')
import os.path


class main_tab:
    def __init__(self ):
        self.credentials=[]
        logout_page = st.Page(self.logout, title="Log out")
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
            pg = st.navigation([st.Page(self.login)])

        pg.run()

    def logout(self):
        st.session_state.user = None
        st.rerun()

    def login(self):

        st.header("Log in")
        self.username = st.text_input("enter username")
        self.password = st.text_input("enter password")
        col1, col2 = st.columns([1, 1])  # Adjust column ratios as needed

        with col1:
            if st.button("Log in", use_container_width=True):
                self.checker(self.username, self.password)

        with col2:
            if st.button("Register", use_container_width=True):
                self.retrieve_credentials()
                if self.username in [row[0] for row in self.credentials]:
                    st.warning("this username already exist, try a different one")
                    return
                if self.username == "" or self.password == "":
                    st.warning("one or more of the fields are blank, please add some text")
                else:
                    self.add_credentials(self.username, self.password)
                    st.rerun()
