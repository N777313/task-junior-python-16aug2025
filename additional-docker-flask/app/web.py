from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

DB_SETTINGS = dict(
    dbname=os.getenv("POSTGRES_DB", "appdb"),
    user=os.getenv("POSTGRES_USER", "app"),
    password=os.getenv("POSTGRES_PASSWORD", "app"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=int(os.getenv("POSTGRES_PORT", 5432)),
)

def get_connection():
    return psycopg2.connect(**DB_SETTINGS)

@app.route("/")
def index():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, price, quantity FROM products ORDER BY id")
            products = cur.fetchall()
    return render_template("index.html", products=products)

@app.route("/low-stock")
def low_stock():
    threshold = int(request.args.get("threshold", 10))
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, price, quantity FROM products WHERE quantity < %s", (threshold,))
            products = cur.fetchall()
    return render_template("index.html", products=products, low_stock=True, threshold=threshold)

@app.route("/update/<int:product_id>", methods=["GET", "POST"])
def update(product_id):
    if request.method == "POST":
        new_price = float(request.form["price"])
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE products SET price = %s WHERE id = %s", (new_price, product_id))
                conn.commit()
        return redirect(url_for("index"))
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, price FROM products WHERE id = %s", (product_id,))
            product = cur.fetchone()
    return render_template("update.html", product=product)
