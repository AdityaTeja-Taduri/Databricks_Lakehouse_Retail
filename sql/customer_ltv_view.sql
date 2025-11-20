CREATE OR REPLACE VIEW workspace.gold.vw_customer_lifetime_value AS
SELECT
  customer_id,
  order_count,
  total_spend,
  avg_order_amount,
  first_order_date,
  last_order_date,
  customer_lifetime_days,
  avg_days_between_orders
FROM workspace.gold.customer_lifetime_value;
