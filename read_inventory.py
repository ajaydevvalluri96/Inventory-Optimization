
import pandas as pd

# Read the Excel file
inventory = pd.read_excel("inventory_data.xlsx")

# Display the first five rows
print("\nFIRST FIVE PRODUCTS")
print(inventory.head())

# Count the products
print("\nTOTAL PRODUCTS:", len(inventory))

# Display the Excel column names
print("\nEXCEL COLUMN NAMES")
print(inventory.columns.tolist())
