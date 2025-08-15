#!/usr/bin/env python3
from statistics import mean

employees = [ 
    {"name": "Иван", "position": "разработчик", "salary": 55000}, 
    {"name": "Анна", "position": "аналитик", "salary": 48000}, 
    {"name": "Петр", "position": "тестировщик", "salary": 52000}, 
] 

def analyze_employees(items):
    high_paid_names = [e["name"] for e in items if e["salary"] > 50000]
    avg_salary = mean(e["salary"] for e in items) if items else 0
    sorted_desc = sorted(items, key=lambda e: e["salary"], reverse=True)
    return high_paid_names, avg_salary, sorted_desc


if __name__ == "__main__":
    high_paid, avg_sal, sorted_list = analyze_employees(employees)
    print("1) Имена с зарплатой > 50 000:", high_paid)
    print("2) Средняя зарплата:", avg_sal)
    print("3) Сортировка по зарплате (убывание):")
    for e in sorted_list:
        print(e)
