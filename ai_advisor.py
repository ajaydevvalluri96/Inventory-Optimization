
import json

# STEP 1: Read the JSON inventory data
with open("ai_inventory_data.json", "r", encoding="utf-8") as file:
    products = json.load(file)

print("\nAI INVENTORY BUSINESS ADVISOR")
print("--------------------------------")

# STEP 2: Analyze the first five products
for product in products[:5]:

    name = product["product"]
    stock = product["current_stock"]
    reorder_point = product["reorder_point"]
    order_quantity = product["recommended_order_quantity"]
    supplier = product["supplier"]

    print("\nProduct:", name)
    print("Current Stock:", stock)
    print("Reorder Point:", reorder_point)

    # STEP 3: Generate rule-based recommendations
    if stock <= reorder_point:

        print("Recommendation: REORDER NOW")
        print("Suggested Order Quantity:", order_quantity)
        print("Supplier:", supplier)

        if stock < reorder_point * 0.5:
            print("Priority: HIGH")
            print("Action: Check for urgent replenishment.")
        else:
            print("Priority: NORMAL")
            print("Action: Schedule replenishment.")

    else:
        print("Recommendation: Stock is sufficient.")

print("\nBusiness analysis completed!")
