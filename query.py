from sqlalchemy import URL, create_engine, text
import pandas as pd

# enter your localhost information to connect to the database
username = "root"
password = "F.a0480795444"
host = "127.0.0.1"
port = 3306
database_name = "cosmetics_shop"


url_object = URL.create(
    drivername="mysql+pymysql",
    username=username,
    password=password,
    host=host,
    port=port,
    database=database_name,
)


# return connection object
def get_connection(url_object=url_object):
    engine = create_engine(url_object)
    connection = engine.connect()
    return connection


# return DataFrame object of the query
def get_query(connection, query):
    result = connection.execute(text(f"{query}"))
    return pd.DataFrame(result)


# TODO function to return pandas datadrame based on CursorResult object
