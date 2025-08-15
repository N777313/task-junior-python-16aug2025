#!/usr/bin/env python3
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_suffix(".db")

def setup_db(conn):
    cur = conn.cursor()
    print("Создаю таблицу employees ...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            salary INTEGER NOT NULL
        )
    """)
    conn.commit()

def seed_data(conn):
    cur = conn.cursor()
    print("Вставляю 5 тестовых записей ...")
    cur.executemany(
        "INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)",
        [
            ("Иван", "разработчик", 55000),
            ("Анна", "аналитик", 48000),
            ("Петр", "тестировщик", 52000),
            ("Мария", "дизайнер", 50000),
            ("Сергей", "тимлид", 90000),
        ],
    )
    conn.commit()

def select_high_salary(conn, threshold=50000):
    print(f"Сотрудники с зарплатой > {threshold}:")
    cur = conn.cursor()
    for row in cur.execute("SELECT id, name, position, salary FROM employees WHERE salary > ?", (threshold,)):
        print(row)

def update_ivan(conn):
    print("Обновляю зарплату Ивану до 60000 ...")
    cur = conn.cursor()
    cur.execute("UPDATE employees SET salary = 60000 WHERE name = ?", ("Иван",))
    conn.commit()

def delete_anna(conn):
    print("Удаляю Анну ...")
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE name = ?", ("Анна",))
    conn.commit()

def dump_all(conn, label):
    print(f"\n[{label}] Текущее состояние таблицы:")
    for row in conn.execute("SELECT id, name, position, salary FROM employees ORDER BY id"):
        print(row)

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    try:
        setup_db(conn)
        seed_data(conn)
        dump_all(conn, "после вставки")
        select_high_salary(conn, 50000)
        update_ivan(conn)
        delete_anna(conn)
        dump_all(conn, "после обновления и удаления")
    finally:
        conn.close()
        print("\nГотово.")
