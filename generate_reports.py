import csv
import sqlite3
from datetime import datetime

# Connect to the clean database created by etl_pipeline.py
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Define the reports and their corresponding SQL queries
reports = {
    "low_stock_alerts.csv": """
        SELECT 
            sku AS "SKU",
            item_name AS "Item Name",
            warehouse_zone AS "Zone",
            stock_qty AS "Current Stock",
            reorder_level AS "Reorder Threshold",
            (reorder_level - stock_qty) AS "Units Needed"
        FROM inventory
        WHERE stock_qty <= reorder_level
        ORDER BY (reorder_level - stock_qty) DESC;
    """,
    "zone_valuation_summary.csv": """
        SELECT 
            warehouse_zone AS "Warehouse Zone",
            COUNT(sku) AS "Unique SKUs",
            SUM(stock_qty) AS "Total Units",
            PRINTF('$%.2f', SUM(stock_qty * unit_cost)) AS "Total Inventory Value"
        FROM inventory
        GROUP BY warehouse_zone
        ORDER BY SUM(stock_qty * unit_cost) DESC;
    """,
    "high_value_stock.csv": """
        SELECT 
            sku AS "SKU",
            item_name AS "Item Name",
            stock_qty AS "Current Stock",
            PRINTF('$%.2f', unit_cost) AS "Unit Cost",
            PRINTF('$%.2f', stock_qty * unit_cost) AS "Total Item Value"
        FROM inventory
        WHERE (stock_qty * unit_cost) > 1000
        ORDER BY (stock_qty * unit_cost) DESC;
    """
}

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"--- Generating Operations Reports ({timestamp}) ---")

for filename, query in reports.items():
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Extract column headers directly from the SQL query aliases
    headers = [description[0] for description in cursor.description]
    
    # Write headers and query results to a CSV file (opens cleanly in Excel)
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
        
    print(f"Exported {filename} ({len(rows)} rows)")

conn.close()
print("--- All reports generated successfully. ---")
