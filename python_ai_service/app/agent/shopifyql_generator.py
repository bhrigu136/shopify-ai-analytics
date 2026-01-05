import re

def generate_shopifyql(intent_dict: dict, question: str) -> str:
    intent = intent_dict.get("intent")
    detail = intent_dict.get("detail")
    entities = intent_dict.get("entities", {})
    period = entities.get("period_days", 30)
    product_name = entities.get("product")

    # Specific Product Sales/Inventory
    if intent == "sales" and detail == "product_performance" and product_name:
        return (
            f"SELECT product_title, SUM(quantity) AS total_sold "
            f"FROM orders "
            f"WHERE created_at >= -{period}d AND product_title LIKE '%{product_name}%' "
            f"GROUP BY product_title"
        )

    # Top Products (General)
    if intent == "sales" and detail == "top_products":
        return (
            f"SELECT product_title, SUM(quantity) AS total_sold "
            f"FROM orders "
            f"WHERE created_at >= -{period}d "
            f"GROUP BY product_title "
            f"ORDER BY total_sold DESC "
            f"LIMIT 5"
        )

    # Inventory Projection
    if intent == "inventory" and detail == "inventory_projection":
        query = (
            f"SELECT product_id, product_title, SUM(quantity) AS total_sold_period "
            f"FROM orders "
            f"WHERE created_at >= -{period}d "
        )
        if product_name:
            query += f"AND product_title LIKE '%{product_name}%' "
        
        query += "GROUP BY product_id, product_title"
        return query

    # ... (existing customers logic) ...
    if intent == "customers" and detail == "repeat_customers":
        return (
            f"SELECT customer_id, COUNT(order_id) AS orders_count "
            f"FROM orders "
            f"WHERE created_at >= -{period}d "
            f"GROUP BY customer_id "
            f"HAVING orders_count > 1"
        )

    return "-- SHOPIFYQL: fallback/unknown"

def validate_shopifyql(query: str) -> bool:
    # Validates the generated ShopifyQL query for safety and basic syntax.
    
    # Normalize query for checking
    q_upper = query.upper().strip()

    # Basic Structure Check
    if not q_upper.startswith("SELECT"):
        print("Validation Failed: Query must start with SELECT.")
        return False
    
    if " FROM " not in q_upper:
        print("Validation Failed: Query must contain a FROM clause.")
        return False

    # Safety Check: Forbidden Keywords (Destructive operations)
    forbidden_keywords = ["DELETE", "DROP", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "GRANT", "REVOKE"]
    for word in forbidden_keywords:
        if re.search(r'\b' + word + r'\b', q_upper):
            print(f"Validation Failed: Forbidden keyword detected: {word}")
            return False

    # Syntax Check: Balanced Parentheses
    if q_upper.count("(") != q_upper.count(")"):
        print("Validation Failed: Unbalanced parentheses.")
        return False

    return True