-- Query 1: Low-Stock Reorder Alert Report
-- Identifies items at or below minimum threshold and calculates units needed
SELECT 
    sku,
    item_name,
    warehouse_zone,
    stock_qty,
    reorder_level,
    (reorder_level - stock_qty) AS deficit_units
FROM inventory
WHERE stock_qty <= reorder_level
ORDER BY deficit_units DESC;

-- Query 2: Total Inventory Valuation by Warehouse Zone
-- Summarizes unit count and dollar value per zone for management reporting
SELECT 
    warehouse_zone,
    COUNT(sku) AS unique_skus,
    SUM(stock_qty) AS total_units,
    ROUND(SUM(stock_qty * unit_cost), 2) AS total_zone_value
FROM inventory
GROUP BY warehouse_zone
ORDER BY total_zone_value DESC;

-- Query 3: High-Value Stock Concentration
-- Flags items tying up more than $1,000 in capital
SELECT 
    sku,
    item_name,
    stock_qty,
    unit_cost,
    ROUND(stock_qty * unit_cost, 2) AS total_item_value
FROM inventory
WHERE (stock_qty * unit_cost) > 1000
ORDER BY total_item_value DESC;
