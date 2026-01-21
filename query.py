from sqlalchemy import URL, create_engine, text
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
table = serv["table"]


def get_connection(url_object=url_object):
    """Create an _engine.Connection object for interaction
    with database specified in config.toml"""
    engine = create_engine(url_object)
    connection = engine.connect()
    return connection


def column_values(connection, columns):
    """
    Return a list where each element is a list,
    consisting of all values from a table's column

    :param engine: SQLAlchemy _engine.Engine object
    :param query: Space separated string of columns
    you want to get the values from
    """
    result = []
    for column in columns.split(" "):
        column_values = connection.execute(text(f"select {column} from {table}"))
        result.append(column_values.scalars().all())
    return result

# Edit later:
# To get all unique products
def get_all_unique_products(connection):
    sql = f"""
    SELECT *
    FROM {table}
    """
    result=connection.execute(text(sql))
    return result.mappings().all()
