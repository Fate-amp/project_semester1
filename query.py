from sqlalchemy import URL, create_engine, text
import tomllib
from sqlalchemy.orm import sessionmaker
from product import Product
from sqlalchemy import or_, asc, desc,func

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
    list of column names (strings) -> list of lists of values of given columns
    Return a list where each element is a list,
    consisting of all values from a table's column 
    (defined either by table column's name or a query).

    :param connection: SQLAlchemy _engine.Connection object
    :param columns: List of columns (strings)
    you want to get the values from. Alternatively
    columns can be a list of queries to be pasted into
    "select {column} from {table}" template. Can be useful
    to fetch multiple lists of values at once.
    """
    result = []
    for column in columns:
        column_values = connection.execute(text(f"select {column} from {table}"))
        result.append(column_values.scalars().all())
    return result

def just_execute(connection, query):
    '''
    query string -> list of lists of columns of output table
    General purpose function for executing queries and returning lists with column values.
    In your query string use should use _table_ keyword if you want this
    function to automatically replace it with table name provided in config.toml
    
    :param connection: SQLAlchemy _engine.Connection object
    :param query: string with SQL query
    '''
    query = query.replace("_table_", table)
    cursor = connection.execute(text(query))
    rows = cursor.all() #function works with any amount of columns in the output table
    return list(map(list, zip(*rows))) 


# Following creates an engine
def get_engine(url_object=url_object):
    return create_engine(url_object)
engine = get_engine()
# The following lines are to create a session
Session=sessionmaker(bind=engine)
session=Session()
# The following function will apply filtering, sorting and searching and paginates the result

from sqlalchemy import or_, asc, desc

def get_products_paginated(page=1, search_key=None, category=None, sort=None):
    offset = (page - 1) * 20

    # Start the query
    query = session.query(Product)

    # --- Search ---
    if search_key:
        pattern = f"%{search_key}%"
        query = query.filter(
            or_(
                Product.product_name.ilike(pattern),
                Product.brand.ilike(pattern)
            )
        )

    # --- Category filter ---
    if category and category != "All":
        query = query.filter(Product.category == category)

    # --- Sorting ---
    if sort == "price_asc":
        query = query.order_by(asc(Product.price))
    elif sort == "price_desc":
        query = query.order_by(desc(Product.price))
    elif sort == "popular":
        query = query.order_by(desc(Product.rating))
    elif sort == "name_desc":
        query = query.order_by(desc(Product.product_name))
    elif sort == "name_desc":
        query = query.order_by(desc(Product.product_name))
    else:  # default
        query = query

    # --- Count total for pagination ---
    total = query.count()  # SQLAlchemy handles subquery quoting correctly

    # --- Pagination ---
    products = query.offset(offset).limit(20).all()  # per_page is always 20

    return products, total
