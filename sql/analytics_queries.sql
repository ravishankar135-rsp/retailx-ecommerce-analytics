-- ============================================================
-- RetailX - SQL Analytics Layer
-- E-Commerce Sales & Inventory Analytics
-- ============================================================

USE retailx;


-- ============================================================
-- 1. Overall Sales KPI
-- ============================================================

SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(net_revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(net_revenue), 2) AS average_order_value,
    ROUND(
        SUM(profit) / NULLIF(SUM(net_revenue), 0) * 100,
        2
    ) AS profit_margin_pct
FROM orders;


-- ============================================================
-- 2. Monthly Sales Analysis
-- ============================================================

SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
    COUNT(*) AS total_orders,
    ROUND(SUM(net_revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY sales_month;


-- ============================================================
-- 3. Product Performance
-- ============================================================

SELECT
    product_id,
    product,
    category,
    SUM(quantity) AS units_sold,
    ROUND(SUM(net_revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) / NULLIF(SUM(net_revenue), 0) * 100,
        2
    ) AS profit_margin_pct
FROM orders
GROUP BY
    product_id,
    product,
    category
ORDER BY revenue DESC;


-- ============================================================
-- 4. Top 3 Products per Category
-- Window Function: DENSE_RANK
-- ============================================================

WITH ranked_products AS (
    SELECT
        product_id,
        product,
        category,
        revenue,
        profit,
        DENSE_RANK() OVER (
            PARTITION BY category
            ORDER BY revenue DESC
        ) AS revenue_rank
    FROM vw_product_performance
)
SELECT
    product_id,
    product,
    category,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    revenue_rank
FROM ranked_products
WHERE revenue_rank <= 3
ORDER BY category, revenue_rank;


-- ============================================================
-- 5. Top 10 Customers
-- CTE + Window Function
-- ============================================================

WITH customer_sales AS (
    SELECT
        customer_id,
        customer_name,
        COUNT(*) AS total_orders,
        SUM(quantity) AS units_purchased,
        ROUND(SUM(net_revenue), 2) AS total_revenue,
        ROUND(SUM(profit), 2) AS total_profit
    FROM orders
    GROUP BY
        customer_id,
        customer_name
),
ranked_customers AS (
    SELECT
        *,
        DENSE_RANK() OVER (
            ORDER BY total_revenue DESC
        ) AS revenue_rank
    FROM customer_sales
)
SELECT
    customer_id,
    customer_name,
    total_orders,
    units_purchased,
    total_revenue,
    total_profit,
    revenue_rank
FROM ranked_customers
WHERE revenue_rank <= 10
ORDER BY revenue_rank;


-- ============================================================
-- 6. Customer Segmentation
-- CASE WHEN + CTE
-- ============================================================

WITH customer_sales AS (
    SELECT
        customer_id,
        customer_name,
        COUNT(*) AS total_orders,
        ROUND(SUM(net_revenue), 2) AS total_revenue,
        ROUND(SUM(profit), 2) AS total_profit
    FROM orders
    GROUP BY
        customer_id,
        customer_name
),
segmented_customers AS (
    SELECT
        *,
        CASE
            WHEN total_revenue >= 100000 THEN 'High Value'
            WHEN total_revenue >= 50000 THEN 'Medium Value'
            ELSE 'Low Value'
        END AS customer_segment
    FROM customer_sales
)
SELECT
    customer_segment,
    COUNT(*) AS customers,
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    ROUND(AVG(total_revenue), 2) AS avg_customer_revenue
FROM segmented_customers
GROUP BY customer_segment
ORDER BY total_revenue DESC;


-- ============================================================
-- 7. Inventory Risk Analysis
-- ============================================================

SELECT
    product_id,
    product,
    category,
    warehouse,
    stock_quantity,
    reorder_level,
    reorder_quantity,
    units_sold,
    ROUND(revenue, 2) AS revenue,
    risk_score
FROM inventory_risk_view
ORDER BY
    risk_score DESC,
    revenue DESC
LIMIT 15;


-- ============================================================
-- 8. Warehouse Risk Analysis
-- ============================================================

SELECT
    warehouse,
    COUNT(*) AS inventory_items,
    SUM(stock_quantity) AS stock_units,
    ROUND(SUM(revenue), 2) AS revenue,
    SUM(risk_score) AS total_risk_score,
    ROUND(AVG(risk_score), 2) AS avg_risk_score
FROM inventory_risk_view
GROUP BY warehouse
ORDER BY total_risk_score DESC;


-- ============================================================
-- 9. Category Inventory Risk
-- ============================================================

SELECT
    category,
    COUNT(*) AS inventory_items,
    SUM(stock_quantity) AS stock_units,
    ROUND(SUM(revenue), 2) AS revenue,
    SUM(risk_score) AS total_risk_score
FROM inventory_risk_view
GROUP BY category
ORDER BY total_risk_score DESC;


-- ============================================================
-- 10. Reorder Priority Analysis
-- CTE + CASE WHEN
-- ============================================================

WITH reorder_analysis AS (
    SELECT
        product_id,
        product,
        category,
        warehouse,
        stock_quantity,
        reorder_level,
        reorder_quantity,
        units_sold,
        revenue,
        risk_score,

        CASE
            WHEN stock_quantity = 0 THEN 'CRITICAL'
            WHEN stock_quantity <= reorder_level
                 AND risk_score >= 70 THEN 'HIGH'
            WHEN stock_quantity <= reorder_level THEN 'MEDIUM'
            ELSE 'LOW'
        END AS reorder_priority

    FROM inventory_risk_view
)
SELECT
    product_id,
    product,
    category,
    warehouse,
    stock_quantity,
    reorder_level,
    reorder_quantity,
    risk_score,
    reorder_priority
FROM reorder_analysis
WHERE reorder_priority IN ('CRITICAL', 'HIGH', 'MEDIUM')
ORDER BY
    CASE reorder_priority
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MEDIUM' THEN 3
    END,
    risk_score DESC;