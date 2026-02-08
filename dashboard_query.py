import query

# utility script for specified queries for dashboard. call functions with _engine.Connection SQLAlchemy object

def list_to_float(li):
    '''
    Transform a list of decimals into list of floats. We need this because for some values in our database,
    SQLAlchemy returns decimal type variables
    
    :param li: list with decimal type objects
    '''
    for i in range(len(li)):
        li[i] = float(li[i])
    return li


# following functions can be used to pass data to chart.js

def price_hist(connection, pr_ranges):
    '''
    Return list with counts of prices for given prices ranges.

    :param connection: _engine.Connection object
    :param ranges: List of prices ranges to count. Represent ranges with lists or tuples
    E.g.: [[10,100], [100, 500], [500]] -> count of prices between 10 and 100, between 100 and 500, from 500 to max
    Single values will be interpreted as range from given number to plus infinity. [500] = from 500 to infinity

    '''

    columns = [] #generate a list columns to paste into query.
    for pr_range in pr_ranges:
        if len(pr_range) == 2:
            columns.append(f"count(CASE WHEN price >= {pr_range[0]} AND price < {pr_range[1]} THEN 1 END)")
        elif len(pr_range) == 1:
            columns.append(f"count(CASE WHEN price >= {pr_range[0]} THEN 1 END)")
        else:
            raise ValueError("pr_ranges follows incorrect syntax")

    prices = query.column_values(connection, columns)
    return [price[0] for price in prices] #column_values returns a list of lists, while we want a list of integers here


def rating_by_brand(connection):
    '''
    Return a list with the 1st element being a list of all brands and the 2nd being a list of their corresponding scores 
    calculated based on average rating and amount of ratings. The function uses log so that brands can't get overblown scores 
    just by having a big amount of reviews. The bigger the score, the more confident we can be in the brand.

    Example: 
    result = rating_by_brand(connection)
    
    brands, scores = ratings[0], ratings[1]
    
    :param connection: _engine.Connection object
    '''

    res = query.just_execute(connection, "select brand, round(avg(rating) * log(sum(noofratings)+1)) as score from _table_ where rating >= 1 and rating <= 5 and noofratings is not null group by replace(lower(brand), ' ', '') order by score asc")
    return res

    
def reviews_by_country(connection, floor):
    '''
    Ratio of positive reviews per country (any review >= floor is considered positive).

    Example:
    result = reviews_by_country(connection, 3.5)

    countries, ratios = result[0], result[1]
    
    :param connection: _engine.Connection object
    '''

    countries, ratios = query.just_execute(connection, f"select country, round(sum(rating)/count(rating),2) from _table_ where rating > {floor} group by country order by country desc")
  
    return [countries, list_to_float(ratios)]


# following functions provide general statistics to be displayed on dashboard

def best_brands(brands, scores, n):
    '''
    Return best n amount of brands, based on their scores.
    Output data structure is a list of tuples where each tuple
    is a pair of brand and it's corresponsing rating. The list is sorted
    by ratings descending
    
    :param brands: list of brands
    :param scores: list of scores
    '''

    top_brands = [(brand, score) for brand, score in sorted(zip(brands, scores), key = lambda pair: pair[1], reverse=True)] # sort by rating
    return top_brands[:n]


def country_list(connection):
    '''
    Return unique countries from dataset
    
    :param connection: _engine.Connection object
    '''
    countries = query.just_execute(connection, "select distinct country from _table_")
    return countries[0] # just_execute returns a nested list


def country_stats(connection, country, n):
    '''
    Return most popular brands and subcategories (by number of ratings) and number of products in a given country.
    n restricts the amount of output values (except for number of products which is always one)

    Example:
    result = country_stats(connection, "India", 5)

    top_brands_india = result[0] # list of strings
    top_categories_india = result[1] # list of integers
    product_count_india = result[2] # integer
    
    :param connection: _engine.Connection object
    :param country: choose a country out of country table to fetch statistics for
    '''

    brands = query.just_execute(connection, f"select brand from _table_ where country = '{country}' group by replace(lower(brand), ' ', '') order by sum(noofratings) desc limit {n}")    
    subcategories = query.just_execute(connection, f"select subcategory from _table_ where country = '{country}' group by replace(lower(subcategory), ' ', '') order by count(subcategory) desc limit {n}")
    products_count = query.just_execute(connection, f"select count(distinct product_name) from _table_ where country = '{country}'")

    return brands + subcategories + products_count[0]