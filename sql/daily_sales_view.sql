CREATE OR REPLACE VIEW workspace.gold.vw_daily_sales AS
SELECT
  order_date,
  total_orders,
  total_quantity,
  total_revenue,
  avg_order_value
FROM workspace.gold.daily_sales;
