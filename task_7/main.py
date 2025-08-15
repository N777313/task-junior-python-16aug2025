#!/usr/bin/env python3
import argparse, os, time
import psycopg2

DB_SETTINGS = dict(
    dbname=os.getenv("POSTGRES_DB", "appdb"),
    user=os.getenv("POSTGRES_USER", "app"),
    password=os.getenv("POSTGRES_PASSWORD", "app"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=int(os.getenv("POSTGRES_PORT", "5432")),
)

def connect():
    return psycopg2.connect(**DB_SETTINGS)

def init_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                price NUMERIC(10,2) NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)
        conn.commit()

def seed_data(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM products")
        (count,) = cur.fetchone()
        if count == 0:
            print("Вставляю 10 тестовых продуктов ...")
            for i in range(1, 11):
                cur.execute(
                    "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)",
                    (f"Product {i}", 9.99 * i, 5 + i),
                )
            conn.commit()
        else:
            print(f"Данные уже есть: {count} записей.")

def low_stock(conn, threshold=10):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, price, quantity FROM products WHERE quantity < %s ORDER BY quantity ASC",
            (threshold,),
        )
        rows = cur.fetchall()
        print(f"Товары с количеством < {threshold}: {len(rows)}")
        for r in rows:
            print(r)

def update_price(conn, name, price):
    with conn.cursor() as cur:
        cur.execute("UPDATE products SET price = %s WHERE name = %s", (price, name))
        conn.commit()
        print(f"Обновлено строк: {cur.rowcount}")

def main():
    parser = argparse.ArgumentParser(description="task_7: PostgreSQL CRUD")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="создать таблицу и вставить тестовые данные")
    p_low = sub.add_parser("low-stock", help="список товаров с количеством < 10")
    p_low.add_argument("--threshold", type=int, default=10)
    p_upd = sub.add_parser("update-price", help="обновить цену по имени")
    p_upd.add_argument("--name", required=True)
    p_upd.add_argument("--price", type=float, required=True)

    args = parser.parse_args()

    conn = None
    try:
        conn = connect()
        if args.cmd == "init":
            init_db(conn)
            seed_data(conn)
        elif args.cmd == "low-stock":
            low_stock(conn, args.threshold)
        elif args.cmd == "update-price":
            update_price(conn, args.name, args.price)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
