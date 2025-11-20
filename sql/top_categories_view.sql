CREATE OR REPLACE VIEW workspace.gold.vw_top_categories AS
SELECT
  category,
  category_revenue,
  orders,
  units_sold,
  revenue_rank
FROM workspace.gold.top_categories;
