import os

import pymysql
from google.cloud.sql.connector import Connector
import google.auth
from google.auth.transport.requests import Request
import sqlalchemy

# IAM database user parameter (IAM user's email before the "@" sign, mysql truncates usernames)
# ex. IAM user with email "demo-user@test.com" would have database username "demo-user"
IAM_USER = "blackelm"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ="application_default_credentials.json"
# initialize connector
connector = Connector()

# getconn now using IAM user and requiring no password with IAM Auth enabled
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