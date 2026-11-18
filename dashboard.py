
import os
import pandas as pd
import streamlit as st
import anthropic

# ------------------------------------
# PAGE CONFIGURATION
# ------------------------------------

st.set_page_config(
    page_title="AI Inventory Optimization Dashboard",
    page_icon="📦",
    layout="wide"
)

st.title("📦 AI Inventory Optimization Dashboard")

st.write(
    "Inventory optimization using Python, "
    "Operations Research, and Claude AI."
)

# ------------------------------------
# LOAD INVENTORY DATA
# ------------------------------------

@st.cache_data
def load_inventory():
    return pd.read_excel("inventory_optimized.xlsx")


try:
    inventory = load_inventory()
except FileNotFoundError:
    st.error(
        "inventory_optimized.xlsx was not found. "
        "Run optimize_inventory.py first."
    )
    st.stop()

# ------------------------------------
# INVENTORY SUMMARY
# ------------------------------------

total_products = len(inventory)

reorder_count = (
    inventory["Inventory Decision"] == "REORDER NOW"
).sum()

sufficient_count = (
    inventory["Inventory Decision"] == "SUFFICIENT STOCK"
).sum()

st.header("📊 Inventory Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Products", total_products)
col2.metric("Reorder Alerts", int(reorder_count))
col3.metric("Sufficient Stock", int(sufficient_count))

# ------------------------------------
# INVENTORY FILTERS
# ------------------------------------

st.header("🔎 Inventory Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)

categories = ["All"] + sorted(
    inventory["Category"].dropna().unique().tolist()
)

suppliers = ["All"] + sorted(
    inventory["Supplier"].dropna().unique().tolist()
)

statuses = ["All"] + sorted(
    inventory["Inventory Decision"].dropna().unique().tolist()
)

with filter_col1:
    selected_category = st.selectbox(
        "Category",
        categories
    )

with filter_col2:
    selected_supplier = st.selectbox(
        "Supplier",
        suppliers
    )

with filter_col3:
    selected_status = st.selectbox(
        "Inventory Status",
        statuses
    )

filtered_inventory = inventory.copy()

if selected_category != "All":
    filtered_inventory = filtered_inventory[
        filtered_inventory["Category"] == selected_category
    ]

if selected_supplier != "All":
    filtered_inventory = filtered_inventory[
        filtered_inventory["Supplier"] == selected_supplier
    ]

if selected_status != "All":
    filtered_inventory = filtered_inventory[
        filtered_inventory["Inventory Decision"] == selected_status
    ]

# ------------------------------------
# INVENTORY TABLE
# ------------------------------------

st.header("📋 Inventory Data")

st.dataframe(
    filtered_inventory,
    use_container_width=True
)

# ------------------------------------
# INVENTORY STATUS CHART
# ------------------------------------

st.header("📈 Inventory Status")

status_counts = (
    filtered_inventory["Inventory Decision"]
    .value_counts()
)

st.bar_chart(status_counts)

# ------------------------------------
# REORDER ALERTS
# ------------------------------------

st.header("🚨 Products Requiring Reorder")

reorder_products = filtered_inventory[
    filtered_inventory["Inventory Decision"] == "REORDER NOW"
]

st.dataframe(
    reorder_products,
    use_container_width=True
)

# ------------------------------------
# FINANCIAL ANALYSIS
# ------------------------------------

st.header("💰 Financial Analysis")

inventory = inventory.copy()

inventory["Inventory Value"] = (
    inventory["Current Stock"]
    * inventory["Unit Purchase Cost ($)"]
)

inventory["EOQ Purchase Cost"] = (
    inventory["EOQ"]
    * inventory["Unit Purchase Cost ($)"]
)

inventory["Potential Revenue"] = (
    inventory["Current Stock"]
    * inventory["Selling Price ($)"]
)

total_inventory_value = inventory["Inventory Value"].sum()

total_replenishment_cost = inventory.loc[
    inventory["Inventory Decision"] == "REORDER NOW",
    "EOQ Purchase Cost"
].sum()

total_potential_revenue = inventory["Potential Revenue"].sum()

fin_col1, fin_col2, fin_col3 = st.columns(3)

fin_col1.metric(
    "Current Inventory Value",
    f"${total_inventory_value:,.2f}"
)

fin_col2.metric(
    "Estimated Replenishment Purchase Cost",
    f"${total_replenishment_cost:,.2f}"
)

fin_col3.metric(
    "Potential Sales Revenue",
    f"${total_potential_revenue:,.2f}"
)

st.caption(
    "Potential revenue assumes all current inventory "
    "is sold at its listed selling price. "
    "Replenishment cost assumes one EOQ-sized order "
    "for each product currently flagged for reorder."
)

# ------------------------------------
# TOP 10 PRODUCTS BY INVENTORY VALUE
# ------------------------------------

st.header("🏆 Top 10 Products by Inventory Value")

top_products = inventory.nlargest(
    10,
    "Inventory Value"
)

st.bar_chart(
    top_products.set_index("Product Name")[
        "Inventory Value"
    ]
)

# ------------------------------------
# CLAUDE AI INVENTORY ADVISOR
# ------------------------------------

st.divider()

st.header("🤖 Claude AI Inventory Advisor")

st.write(
    "Select a product to receive AI-powered "
    "inventory risk analysis and business recommendations."
)

product_options = inventory[
    ["Product ID", "Product Name"]
].drop_duplicates(subset=["Product ID"])

selected_product_id = st.selectbox(
    "Select a product for Claude AI analysis:",
    options=product_options["Product ID"].tolist(),
    format_func=lambda product_id: (
        f"{product_options.loc[product_options['Product ID'] == product_id, 'Product Name'].iloc[0]}"
        f" ({product_id})"
    )
)

selected_product = inventory.loc[
    inventory["Product ID"] == selected_product_id
].iloc[0]

st.subheader("Selected Product Information")

info_col1, info_col2, info_col3 = st.columns(3)

info_col1.metric(
    "Current Stock",
    f"{selected_product['Current Stock']:,.0f} units"
)

info_col2.metric(
    "Reorder Point",
    f"{selected_product['Basic Reorder Point']:,.0f} units"
)

info_col3.metric(
    "Economic Order Quantity",
    f"{selected_product['EOQ']:,.0f} units"
)

st.write(
    "**Inventory Status:**",
    selected_product["Inventory Decision"]
)

if st.button("Analyze Inventory with Claude AI"):

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        st.error(
            "Anthropic API key not found. "
            "Restart Streamlit from the terminal "
            "where the key is loaded."
        )

    else:
        prompt = f"""
You are an inventory management advisor.

Analyze the following inventory data:

Product: {selected_product['Product Name']}
Category: {selected_product['Category']}
Current Stock: {selected_product['Current Stock']} units
Daily Demand: {selected_product['Daily Demand']} units
Supplier Lead Time: {selected_product['Lead Time (Days)']} days
Reorder Point: {selected_product['Basic Reorder Point']} units
Economic Order Quantity: {selected_product['EOQ']:.0f} units
Inventory Status: {selected_product['Inventory Decision']}
Supplier: {selected_product['Supplier']}

Provide a practical business analysis:

1. Explain the current inventory situation.
2. Explain whether reordering is necessary now.
3. Identify potential stockout or excess-stock risks.
4. Explain how the reorder point and EOQ support the decision.
5. Recommend the next action for the inventory manager.

Important:
- Do not automatically recommend reordering.
- If inventory is sufficient, explain why.
- Treat EOQ as an estimated optimal batch size
  under standard EOQ assumptions.
- Do not invent supplier information or demand forecasts.
- Explain in simple business language.
- Keep the response under 200 words.
"""

        try:
            with st.spinner(
                "Claude AI is analyzing the selected product..."
            ):
                client = anthropic.Anthropic(
                    api_key=api_key
                )

                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=350,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

            st.success("Claude AI analysis completed!")

            st.markdown(
                response.content[0].text
            )

        except anthropic.AuthenticationError:
            st.error(
                "Authentication failed. "
                "Check your Anthropic API key."
            )

        except anthropic.RateLimitError:
            st.error(
                "Anthropic rate limit or usage limit reached. "
                "Check your account usage and billing."
            )

        except anthropic.APIConnectionError:
            st.error(
                "Could not connect to Anthropic. "
                "Check your internet connection."
            )

        except anthropic.APIError as error:
            st.error(
                f"Claude API request failed: {error}"
            )

# ------------------------------------
# FOOTER
# ------------------------------------

st.divider()

st.caption(
    "AI Inventory Optimization Project | "
    "Python + Excel + Operations Research + Claude AI"
)
