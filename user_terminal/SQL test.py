from google.cloud.sql.connector import Connector
import pymysql
import sqlalchemy

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

# initialize Cloud SQL Python Connector as context manager
with Connector() as connector:
    # initialize connection pool
    pool = init_connection_pool(connector)
    # insert statement
    insert_stmt = sqlalchemy.text(
        "INSERT INTO my_table (id, title) VALUES (:id, :title)",
    )

    # interact with Cloud SQL database using connection pool
    with pool.connect() as db_conn:
        # insert into database
        db_conn.execute(insert_stmt, parameters={"id": "book1", "title": "Book One"})

        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()

        # query database
        result = db_conn.execute(sqlalchemy.text("SELECT * from my_table")).fetchall()

        # Do something with the results
        for row in result:
            print(row)