from sqlalchemy import URL, create_engine, text
import pandas as pd
import tomllib

# get server configuration from config.toml and load it
with open("config.toml", "rb") as f:
    serv = tomllib.load(f)

url_object = URL.create(
    drivername=serv["drivername"],
    username=serv["username"],
    password=serv["password"],
    host=serv["host"],
    port=serv["port"],
    database=serv["database_name"],
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
