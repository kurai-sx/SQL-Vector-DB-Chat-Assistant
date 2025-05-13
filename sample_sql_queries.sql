
-- SAMPLE SQL QUERIES FOR EACH TABLE

-- USERS
SELECT * FROM users;
SELECT user_id, full_name, email FROM users WHERE created_at >= CURDATE() - INTERVAL 30 DAY;
SELECT COUNT(*) AS total_users FROM users;
SELECT * FROM users WHERE phone LIKE '+91%';
SELECT * FROM users ORDER BY created_at DESC;

-- ADDRESSES
SELECT * FROM addresses;
SELECT DISTINCT city FROM addresses;
SELECT COUNT(*) AS users_per_city, city FROM addresses GROUP BY city;
SELECT a.* FROM addresses a JOIN users u ON a.user_id = u.user_id WHERE u.full_name = 'John Doe';

-- CATEGORIES
SELECT * FROM categories;
SELECT name, description FROM categories;
SELECT c.name, COUNT(p.product_id) AS product_count
FROM categories c
JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_id;

-- PRODUCTS
SELECT * FROM products;
SELECT * FROM products WHERE price > 5000;
SELECT * FROM products WHERE stock = 0;
SELECT name, price FROM products ORDER BY price ASC LIMIT 5;
SELECT p.name, c.name AS category FROM products p JOIN categories c ON p.category_id = c.category_id;

-- CART & CART_ITEMS
SELECT * FROM cart;
SELECT * FROM cart_items;
SELECT ci.cart_id, p.name, ci.quantity FROM cart_items ci JOIN products p ON ci.product_id = p.product_id;
SELECT u.full_name, p.name
FROM cart c
JOIN cart_items ci ON c.cart_id = ci.cart_id
JOIN products p ON p.product_id = ci.product_id
JOIN users u ON c.user_id = u.user_id;

-- ORDERS
SELECT * FROM orders;
SELECT * FROM orders WHERE order_status IN ('pending', 'cancelled');
SELECT u.full_name, o.total_amount FROM users u JOIN orders o ON u.user_id = o.user_id;
SELECT user_id, COUNT(*) AS num_orders FROM orders GROUP BY user_id;

-- ORDER_ITEMS
SELECT * FROM order_items;
SELECT order_id, COUNT(*) AS item_count FROM order_items GROUP BY order_id;
SELECT oi.order_id, p.name, oi.quantity
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id;

-- PAYMENTS
SELECT * FROM payments;
SELECT * FROM payments WHERE payment_status = 'failed';
SELECT payment_method, COUNT(*) AS count FROM payments GROUP BY payment_method;
SELECT o.order_id, p.payment_status, p.paid_at
FROM orders o
JOIN payments p ON o.order_id = p.order_id;

-- JOIN EXAMPLES
-- Get user name, order ID, and delivery city
SELECT u.full_name, o.order_id, a.city
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN addresses a ON o.address_id = a.address_id;

-- Get cart items and total estimated cost
SELECT u.full_name, p.name, ci.quantity, (ci.quantity * p.price) AS estimated_cost
FROM users u
JOIN cart c ON u.user_id = c.user_id
JOIN cart_items ci ON c.cart_id = ci.cart_id
JOIN products p ON p.product_id = ci.product_id;

-- Get order history with item names
SELECT u.full_name, o.order_id, p.name, oi.quantity
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;
