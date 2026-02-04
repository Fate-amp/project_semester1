from flask import Flask, render_template, request
import query
import dashboard_query as dq
app = Flask(__name__)


# create sqlalchemy connection object for later use
connection = query.get_connection()

@app.route("/")
def index():
    return render_template("base.html")


@app.route("/products")
def get_products_page():
    products=query.get_all_unique_products(connection)
    return render_template("products.html", products=products)


@app.route("/dashboard")
def get_dashboard_page():
    # values for price ranges histogram
    ranges = ["10 - 500", "500 - 2500", "2500 - 10000", "10000+"]
    dash_price_ranges = dq.price_hist(connection, [[10,500], [500,2500], [2500, 10000], [10000]])

    # values for rating by brand chart
    brands_ratings = dq.rating_by_brand(connection)
    dash_rating_brands, dash_rating_scores = brands_ratings[0], brands_ratings[1]

    # values for good reviews ratio per country
    review_ratios = dq.reviews_by_country(connection, 3.5)
    dash_ratio_countries, dash_ratio_ratios = review_ratios[0], review_ratios[1]

    # values for best brands statistics
    dash_best_brands = dq.best_brands(dash_rating_brands, dash_rating_scores, 5)

    # values for statistics by country
    india_stats = dq.country_stats(connection, "India", 5)
    usa_stats = dq.country_stats(connection, "USA", 5)
    
    return render_template("dashboard.html")

# The following lines are there so that flask reboots after
# frontend updates. To be deleted on production! Maya
if __name__ == "__main__":
    app.run(debug=True)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True
