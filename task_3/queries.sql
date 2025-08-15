
-- 1. Общая сумма заказов для каждого клиента
SELECT customer_id, SUM(amount) AS total_amount
FROM orders
GROUP BY customer_id;

-- 2. Клиент с максимальной суммой заказов
SELECT customer_id, SUM(amount) AS total_amount
FROM orders
GROUP BY customer_id
ORDER BY total_amount DESC
LIMIT 1;

-- 3. Количество заказов, сделанных в 2023 году
-- Для SQL-диалектов:
--  - PostgreSQL: EXTRACT(YEAR FROM order_date) = 2023
--  - SQLite: CAST(STRFTIME('%Y', order_date) AS INT) = 2023
--  - MySQL: YEAR(order_date) = 2023
SELECT COUNT(*) AS orders_2023
FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2023;

-- 4. Средняя сумма заказа для каждого клиента
SELECT customer_id, AVG(amount) AS avg_amount
FROM orders
GROUP BY customer_id;
