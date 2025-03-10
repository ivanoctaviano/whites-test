-- Enable the tablefunc extension if not already enabled
CREATE EXTENSION IF NOT EXISTS tablefunc;

-- Drop the materialized view if it exists
DROP MATERIALIZED VIEW IF EXISTS unified_sale_matview CASCADE;

-- Create materialized view storing sales data per day
CREATE MATERIALIZED VIEW unified_sale_matview AS
SELECT
    date_order,
    product_id,
    SUM(order_qty) AS total_quantity,
    SUM(total_sales) AS total_sales
FROM (
    -- Sales Orders
    SELECT 
        so.date_order::DATE AS date_order,
        sol.product_id AS product_id,
        sol.product_uom_qty AS order_qty,
        sol.price_subtotal AS total_sales
    FROM sale_order_line sol
    JOIN sale_order so ON sol.order_id = so.id
    WHERE sol.display_type IS NULL AND so.state IN ('sale', 'done')

    UNION ALL

    -- PoS Orders
    SELECT 
        po.date_order::DATE AS date_order,
        pol.product_id AS product_id,
        pol.qty AS order_qty,
        pol.price_subtotal AS total_sales
    FROM pos_order_line pol
    JOIN pos_order po ON pol.order_id = po.id
    WHERE po.state IN ('paid', 'done', 'invoiced')
) AS unified_sales
GROUP BY date_order, product_id;

-- Index for faster filtering by date
CREATE INDEX unified_sale_date_idx ON unified_sale_matview(date_order);