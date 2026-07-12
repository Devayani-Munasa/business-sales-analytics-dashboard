-- ==========================================
-- Business Sales Analytics Dashboard
-- Phase 6 - SQL Analysis Queries
-- Author: Devayani Munasa
-- ==========================================

USE sales_dashboard;

-- ==========================================
-- 1. Total Sales
-- ==========================================
SELECT
    ROUND(SUM(sales), 2) AS total_sales
FROM sales;


-- ==========================================
-- 2. Total Profit
-- ==========================================
SELECT
    ROUND(SUM(profit), 2) AS total_profit
FROM sales;


-- ==========================================
-- 3. Total Orders
-- ==========================================
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM sales;


-- ==========================================
-- 4. Total Quantity Sold
-- ==========================================
SELECT
    SUM(quantity) AS total_quantity
FROM sales;

-- ==========================================
-- 5. Sales by Region
-- ==========================================
SELECT
    region,
    ROUND(SUM(sales), 2) AS total_sales
FROM sales
GROUP BY region
ORDER BY total_sales DESC;


-- ==========================================
-- 6. Profit by Region
-- ==========================================
SELECT
    region,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY region
ORDER BY total_profit DESC;


-- ==========================================
-- 7. Sales by Category
-- ==========================================
SELECT
    category,
    ROUND(SUM(sales), 2) AS total_sales
FROM sales
GROUP BY category
ORDER BY total_sales DESC;


-- ==========================================
-- 8. Profit by Category
-- ==========================================
SELECT
    category,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY category
ORDER BY total_profit DESC;


-- ==========================================
-- 9. Sales by Sub-Category
-- ==========================================
SELECT
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales
FROM sales
GROUP BY sub_category
ORDER BY total_sales DESC;


-- ==========================================
-- 10. Monthly Sales Trend
-- ==========================================
SELECT
    order_month,
    ROUND(SUM(sales), 2) AS total_sales
FROM sales
GROUP BY order_month
ORDER BY FIELD(
    order_month,
    'January','February','March','April',
    'May','June','July','August',
    'September','October','November','December'
);


-- ==========================================
-- 11. Yearly Sales Trend
-- ==========================================
SELECT
    order_year,
    ROUND(SUM(sales), 2) AS total_sales
FROM sales
GROUP BY order_year
ORDER BY order_year;
-- ==========================================
-- 12. Top 10 Customers by Sales
-- ==========================================
SELECT
    customer_name,
    ROUND(SUM(sales), 2) AS total_sales
FROM sales
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 10;


-- ==========================================
-- 13. Top 10 Customers by Profit
-- ==========================================
SELECT
    customer_name,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY customer_name
ORDER BY total_profit DESC
LIMIT 10;


-- ==========================================
-- 14. Top 10 Best Selling Products
-- ==========================================
SELECT
    product_name,
    ROUND(SUM(sales), 2) AS total_sales
FROM sales
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 10;


-- ==========================================
-- 15. Top 10 Most Profitable Products
-- ==========================================
SELECT
    product_name,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY product_name
ORDER BY total_profit DESC
LIMIT 10;


-- ==========================================
-- 16. Top 10 Loss-Making Products
-- ==========================================
SELECT
    product_name,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY product_name
HAVING total_profit < 0
ORDER BY total_profit ASC
LIMIT 10;