import query

# utility script for specified queries for dashboard. call functions with _engine.Connection SQLAlchemy object

'''
ideas: 

charts:
price range histogram - done
rating by brand
product countries pie chart

statistics:
best brands rating wise
popular brands and categories / no of products - by country
'''

def price_hist(connection, pr_ranges):
    '''
    Return list with counts of prices for given prices ranges.

    :param connection: _engine.Connection object
    :param ranges: List of prices ranges to count. Represent ranges with lists or tuples
    E.g.: [[10,100], [100, 500], [500]]
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
    
    :param connection: _engine.Connection object
    '''

    res = query.just_execute(connection, "select brand, round(avg(rating) * log(sum(noofratings)+1),2) as score from _table_ where rating >= 1 and rating <= 5 and noofratings is not null group by replace(lower(brand), ' ', '') order by brand asc")
    return res
    