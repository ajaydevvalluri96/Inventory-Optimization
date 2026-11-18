
import pandas as pd
import numpy as np

# STEP 1: Read business data from Excel
inventory = pd.read_excel("inventory_data.xlsx")

# STEP 2: Calculate annual demand
inventory["Annual Demand"] = (
    inventory["Daily Demand"] * 365
)

# STEP 3: Calculate Economic Order Quantity
inventory["EOQ"] = np.sqrt(
    (
        2
        * inventory["Annual Demand"]
        * inventory["Order Cost ($)"]
    )
    / inventory["Holding Cost ($/Year)"]
)

# STEP 4: Calculate reorder point
inventory["Basic Reorder Point"] = (
    inventory["Daily Demand"]
    * inventory["Lead Time (Days)"]
)

# STEP 5: Calculate days of stock remaining
inventory["Days Remaining"] = (
    inventory["Current Stock"]
    / inventory["Daily Demand"]
)

# STEP 6: Make inventory decisions
inventory["Inventory Decision"] = np.where(
    inventory["Current Stock"]
    <= inventory["Basic Reorder Point"],
    "REORDER NOW",
    "SUFFICIENT STOCK"
)

# STEP 7: Display inventory recommendations
print("\nAI INVENTORY OPTIMIZATION RESULTS")
print("--------------------------------")

print(
    inventory[
        [
            "Product Name",
            "Current Stock",
            "EOQ",
            "Basic Reorder Point",
            "Inventory Decision"
        ]
    ].head(10).to_string(index=False)
)

# STEP 8: Save the results
inventory.to_excel(
    "inventory_optimized.xlsx",
    index=False
)

print("\nOptimization completed!")
print("Results saved to inventory_optimized.xlsx")