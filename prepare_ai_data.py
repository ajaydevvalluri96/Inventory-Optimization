
import pandas as pd
import json

# STEP 1: Read optimized inventory data
inventory = pd.read_excel("inventory_optimized.xlsx")

# STEP 2: Select products needing replenishment
reorder_products = inventory[
    inventory["Inventory Decision"] == "REORDER NOW"
].copy()

# STEP 3: Prepare relevant business information
ai_data = []

for _, product in reorder_products.iterrows():
    ai_data.append({
        "product": product["Product Name"],
        "current_stock": int(product["Current Stock"]),
        "reorder_point": int(product["Basic Reorder Point"]),
        "recommended_order_quantity": round(
            float(product["EOQ"])
        ),
        "supplier": product["Supplier"]
    })

# STEP 4: Save data in JSON format
with open("ai_inventory_data.json", "w", encoding="utf-8") as file:
    json.dump(ai_data, file, indent=4)

# STEP 5: Display summary
print("\nAI INVENTORY DATA PREPARATION")
print("--------------------------------")
print("Total Products:", len(inventory))
print("Products Needing Reorder:", len(reorder_products))
print("JSON File Created: ai_inventory_data.json")

print("\nFirst Three Products:")
print(json.dumps(ai_data[:3], indent=4))
