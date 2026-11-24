import csv

raw_rows = [
    ["sku", "item_name", "warehouse_zone", "stock_qty", "reorder_level", "unit_cost"],
    ["SKU-101", "Hydraulic Brake Valve", "Zone A", "45", "20", "85.50"],
    ["SKU-102", "LED Trailer Tail Light", " zone a ", "12", "25", "18.00"],
    ["SKU-103", "Heavy Duty Ratchet Strap", "Zone B", "150", "50", "14.25"],
    ["SKU-103", "Heavy Duty Ratchet Strap", "Zone B", "150", "50", "14.25"],  # Duplicate
    ["SKU-104", "Air Brake Hose Assembly", "Zone A", "-4", "15", "32.00"],    # Invalid negative qty
    ["SKU-105", "Pallet Wrap Roll 18in", "Zone C", "", "40", "22.50"],        # Missing qty
    ["SKU-106", "Safety Vest High-Vis", "zone c", "85", "30", "9.75"],
    ["SKU-107", "Wheel Bearing Kit", "Zone B", "8", "15", "64.00"],
    ["SKU-108", "Scanner Battery Pack", "Zone C", "19", "20", "45.00"],
]

with open("warehouse_raw.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(raw_rows)

print("Created warehouse_raw.csv successfully.")
