from flask import Flask, render_template, request
from math import ceil
import query
from query import *
import dashboard_query as dq


app = Flask(__name__)


# create sqlalchemy connection object for later use
connection = query.get_connection()


@app.route("/")
def index():
    return render_template("base.html")

@app.route("/products")
def get_products_page():
    search_key = request.args.get("q", "").strip()
    category = request.args.get("category", "All")
    sort_by = request.args.get("sort_by", "all")

    try:
        page = int(request.args.get("page", 1))
    except (ValueError, TypeError):
        page = 1

    products, total = get_products_paginated(
        page=page,
        search_key=search_key,
        category=category,
        sort=sort_by
    )

    total_pages = max(1, ceil(total / 20))
    page = max(1, min(page, total_pages))

    return render_template(
        "products.html",
        products=products,
        current_page=page,
        total_pages=total_pages,
        current_category=category,
        current_sort=sort_by,
        current_search=search_key
    )



@app.route("/dashboard")
def get_dashboard_page():
    # values for price ranges histogram
    ranges = ["10 - 500", "500 - 2000", "2000 - 5000", "5000 - 10000", "10000+"]
    dash_price_ranges = dq.price_hist(
        connection, [[10, 500], [500, 2000], [2000, 5000], [5000, 10000], [10000]]
    )

    # values for rating by brand chart
    brands_ratings = dq.rating_by_brand(connection)

    # values for good reviews ratio per country
    review_ratios = dq.reviews_by_country(connection, 3.5)

    # values for best brands statistics
    top_brands = dq.best_brands(brands_ratings[0], brands_ratings[1], 5)

    # values for statistics by country
    countries = dq.country_list(connection)
    country_stats = []
    for country in countries:
        country_stats.append([country] + dq.country_stats(connection, country, 5))

    return render_template(
        "dashboard.html",
        canv1_x=ranges,
        canv1_y=dash_price_ranges,
        canv2_x=brands_ratings[0],
        canv2_y=brands_ratings[1],
        canv3_x=review_ratios[0],
        canv3_y=review_ratios[1],
        best_brands=top_brands,
        country_info=country_stats
    )



# The following lines are there so that flask reboots after
# frontend updates. To be deleted on production! Maya
if __name__ == "__main__":
    app.run(debug=True)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True
