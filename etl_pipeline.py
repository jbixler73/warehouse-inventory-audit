import csv
import sqlite3

# 1. Connect to SQLite database (creates inventory.db automatically)
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS inventory")
cursor.execute("""
    CREATE TABLE inventory (
        sku TEXT PRIMARY KEY,
        item_name TEXT NOT NULL,
        warehouse_zone TEXT NOT NULL,
        stock_qty INTEGER NOT NULL,
        reorder_level INTEGER NOT NULL,
        unit_cost REAL NOT NULL
    )
""")

seen_skus = set()
clean_records = []
anomalies = []

# 2. Read and clean raw CSV data
with open("warehouse_raw.csv", "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        sku = row["sku"].strip().upper()
        name = row["item_name"].strip()
        zone = row["warehouse_zone"].strip().title()  # Fixes " zone a " -> "Zone A"

        # Check for duplicate SKUs
        if sku in seen_skus:
            anomalies.append((sku, name, "Duplicate SKU removed"))
            continue

        # Validate stock quantity
        try:
            qty = int(row["stock_qty"])
            if qty < 0:
                anomalies.append((sku, name, f"Negative stock quantity ({qty})"))
                continue
        except ValueError:
            anomalies.append((sku, name, "Missing or non-numeric stock quantity"))
            continue

        reorder = int(row["reorder_level"])
        cost = float(row["unit_cost"])

        seen_skus.add(sku)
        clean_records.append((sku, name, zone, qty, reorder, cost))

# 3. Insert clean records into SQL database
cursor.executemany("""
    INSERT INTO inventory (sku, item_name, warehouse_zone, stock_qty, reorder_level, unit_cost)
    VALUES (?, ?, ?, ?, ?, ?)
""", clean_records)

conn.commit()
conn.close()

# 4. Export data anomalies for operations audit
with open("audit_anomalies.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["sku", "item_name", "issue_detected"])
    writer.writerows(anomalies)

print(f"Loaded {len(clean_records)} clean items into inventory.db.")
print(f"Flagged {len(anomalies)} anomalies in audit_anomalies.csv.")
