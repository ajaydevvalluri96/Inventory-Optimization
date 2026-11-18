
# AI Inventory Optimization Project
# Step 4: Business Input Data

# Average number of bags sold each day
daily_demand = 20

# Number of operating days per year
operating_days = 365

# Number of bags currently in the store
current_stock = 80

# Supplier delivery time in days
lead_time = 5

# Cost of placing one purchase order
ordering_cost = 25

# Annual holding cost per bag
holding_cost = 4

# Display the business information
print("AI INVENTORY OPTIMIZATION")
print("--------------------------------")
print("Daily Demand:", daily_demand)
print("Operating Days:", operating_days)
print("Current Stock:", current_stock)
print("Supplier Lead Time:", lead_time)
print("Ordering Cost: $", ordering_cost)
print("Annual Holding Cost: $", holding_cost)


# STEP 5: CALCULATE ANNUAL DEMAND

annual_demand = daily_demand * operating_days

print("--------------------------------")
print("Annual Demand:", annual_demand, "bags")
