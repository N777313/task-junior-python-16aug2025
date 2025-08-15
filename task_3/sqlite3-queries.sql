# Создание таблицы orders
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    amount REAL
);


# Добавим тестовые данные
INSERT INTO orders (customer_id, order_date, amount) VALUES
(1, '2023-01-10', 100.50),
(2, '2023-02-15', 200.75),
(1, '2023-05-20', 150.00),
(3, '2022-12-25', 300.00),
(2, '2023-06-30', 250.00),
(1, '2024-01-01', 400.00),
(3, '2023-03-03', 500.00),
(3, '2023-11-11', 50.00);



# Запрос 1 — Общая сумма заказов для каждого клиента
SELECT customer_id, SUM(amount) AS total_amount
FROM orders
GROUP BY customer_id;


# Запрос 2 — Клиент с максимальной суммой заказов
SELECT customer_id, SUM(amount) AS total_amount
FROM orders
GROUP BY customer_id
ORDER BY total_amount DESC
LIMIT 1;



# Запрос 3 — Количество заказов в 2023 году
SELECT COUNT(*) AS orders_count_2023
FROM orders
WHERE strftime('%Y', order_date) = '2023';


# Запрос 4 — Средняя сумма заказа для каждого клиента
SELECT customer_id, AVG(amount) AS average_order_amount
FROM orders
GROUP BY customer_id;
