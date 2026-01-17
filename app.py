from flask import Flask, render_template
import query

app = Flask(__name__)

# create sqlalchemy connection object for later use
connection = query.get_connection()


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/products")
def get_products_page():
    return render_template("products.html")


@app.route("/dashboard")
def get_dashboard_page():
    result = query.column_values(connection, "price rating")
    return render_template("dashboard.html", prices=result[0], ratings=result[1])


if __name__ == "__main__":
    app.run(debug=True)
