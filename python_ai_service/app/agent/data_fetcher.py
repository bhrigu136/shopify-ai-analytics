# Mocked data fetcher. 
# In a real production app, this would execute the ShopifyQL against the Shopify Admin API.
# Input: shopifyql string (not executed here); output: structured dict
def fetch_shopify_data(shopifyql: str, store_id: str) -> dict:
    
    # Handle specific product sales performance
    # Checks for queries filtering by product title (e.g., "How many units of Product X...")
    if "LIKE" in shopifyql and "total_sold" in shopifyql and "LIMIT" not in shopifyql:
        return {
            "product_performance": {
                "product_title": "Product X (Mocked)", 
                "total_sold": 45,
                "period_days": 30
            }
        }

    # Top Selling Products
    if "SUM(quantity) AS total_sold" in shopifyql and "LIMIT 5" in shopifyql:
        return {
            "top_products": [
                {"product_title": "Classic Latte Mug", "total_sold": 120},
                {"product_title": "Retro Coffee Beans 1kg", "total_sold": 95},
                {"product_title": "Biscotti Pack", "total_sold": 60},
                {"product_title": "Espresso Shot Glass", "total_sold": 42},
                {"product_title": "Reusable Straw Set", "total_sold": 30}
            ],
            "period_days": 7
        }

    # Inventory Projection / Reorder Data
    # Matches the "total_sold_period" alias used in our updated shopifyql_generator
    if "total_sold_period" in shopifyql:
        # Sample aggregated sales for projection calculations
        return {
            "sales_period": [
                {"product_id": 101, "product_title": "Classic Latte Mug", "total_sold_period": 150},
                {"product_id": 102, "product_title": "Retro Coffee Beans 1kg", "total_sold_period": 120},
                {"product_id": 103, "product_title": "Biscotti Pack", "total_sold_period": 90},
            ],
            "period_days": 30
        }
    
    # Legacy check for the old "sales_30d" alias (keeping for backward compatibility if needed)
    if "total_sold_30d" in shopifyql:
        return {
            "sales_30d": [
                {"product_id": 101, "product_title": "Classic Latte Mug", "total_sold_30d": 300},
                {"product_id": 102, "product_title": "Retro Coffee Beans 1kg", "total_sold_30d": 240},
                {"product_id": 103, "product_title": "Biscotti Pack", "total_sold_30d": 90},
            ],
            "period_days": 30,
        }

    # Repeat Customers
    if "orders_count > 1" in shopifyql:
        return {
            "repeat_customers": [
                {"customer_id": 201, "orders_count": 4},
                {"customer_id": 202, "orders_count": 3},
                {"customer_id": 203, "orders_count": 2}
            ],
            "period_days": 90
        }

    # Fallback: empty response
    return {"empty": True}