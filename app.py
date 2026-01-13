from flask import Flask, render_template
import query

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("base.html")

@app.route("/products")
def get_products_page():
    return render_template("products.html")

@app.route("/dashboard")
def get_dashboard_page():
    return render_template("dashboard.html")

# example on how to easily get data from the database
connection = query.get_connection()
get_query = query.get_query(connection, "select product_name from dataset limit 5")
print(get_query)

if __name__ == "__main__":
    app.run(debug=True)
