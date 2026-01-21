from flask import Flask, render_template, request
import query
app = Flask(__name__)


# create sqlalchemy connection object for later use
connection = query.get_connection()


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/products")
def get_products_page():
    products=query.get_all_unique_products(connection)
    return render_template("products.html",products=products)


@app.route("/dashboard")
def get_dashboard_page():
    result = query.column_values(connection, "price rating")
    return render_template("dashboard.html", prices=result[0], ratings=result[1])

# The following lines are there so that flask reboots after
# frontend updates. To be deleted on production! Maya
if __name__ == "__main__":
    app.run(debug=True)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True
