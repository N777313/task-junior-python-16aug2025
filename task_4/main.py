#!/usr/bin/env python3
import argparse, csv, sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_suffix(".db")

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            salary INTEGER NOT NULL
        )
    """)
    conn.commit()

def load_csv(conn, csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [(r["name"], r["position"], int(r["salary"])) for r in reader]
    conn.executemany("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)", rows)
    conn.commit()
    print(f"Загружено {len(rows)} записей из {csv_path}")

def search_by_position(conn, position):
    cur = conn.execute("SELECT id, name, position, salary FROM employees WHERE position = ? ORDER BY salary DESC", (position,))
    result = cur.fetchall()
    print(f"Найдено сотрудников по должности '{position}': {len(result)}")
    for row in result:
        print(row)

def update_salary_by_name(conn, name, salary):
    cur = conn.execute("UPDATE employees SET salary = ? WHERE name = ?", (salary, name))
    conn.commit()
    print(f"Обновлено записей: {cur.rowcount}")

def main():
    parser = argparse.ArgumentParser(description="task_4: CSV -> SQLite + поиск и обновление")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_load = sub.add_parser("load", help="загрузить CSV в базу")
    p_load.add_argument("csv_path", type=str, help="путь к employees.csv")

    p_search = sub.add_parser("search", help="поиск по должности")
    p_search.add_argument("--position", required=True)

    p_update = sub.add_parser("update", help="обновить зарплату по имени")
    p_update.add_argument("--name", required=True)
    p_update.add_argument("--salary", type=int, required=True)

    args = parser.parse_args()

    conn = get_conn()
    try:
        init_db(conn)
        if args.cmd == "load":
            load_csv(conn, args.csv_path)
        elif args.cmd == "search":
            search_by_position(conn, args.position)
        elif args.cmd == "update":
            update_salary_by_name(conn, args.name, args.salary)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
