import re

def classify_intent(question: str) -> dict:
    q = question.lower()
    
    # Default extraction container
    entities = {
        "product": None,
        "period_days": 30  # default to 30 days if no time is specified
    }

    # Extract Period (simple regex for "X days")
    days_match = re.search(r'(\d+)\s*days?', q)
    if days_match:
        entities["period_days"] = int(days_match.group(1))
    elif "next month" in q or "last month" in q:
        entities["period_days"] = 30
    elif "next week" in q or "last week" in q:
        entities["period_days"] = 7
    elif "last 3 months" in q or "90 days" in q:
        entities["period_days"] = 90

    # Extract Product Name (heuristic: text after "product" or "of")
    # Example: "How many units of Product X..." or "sales for product Blue Shirt"
    # This is a basic mock extraction. In production, an LLM would do this.
    product_match = re.search(r'product\s+([a-zA-Z0-9\s]+)', q)
    if product_match:
        # Stop at common auxiliary words to keep the name clean
        raw_name = product_match.group(1)
        # Split by common ending words to isolate the name roughly
        for stopper in [" will", " last", " in", " likely", " go", " do", "?"]:
            raw_name = raw_name.split(stopper)[0]
        entities["product"] = raw_name.strip()

    # 3. Determine Intent
    
    # Inventory / Stock Intent
    if any(k in q for k in ["inventory", "stock", "out of stock", "reorder", "reorder level", "need next"]):
        return {
            "intent": "inventory", 
            "detail": "inventory_projection", 
            "entities": entities
        }
    
    # Sales / Selling Intent
    if any(k in q for k in ["sell", "top selling", "best sellers", "top 5", "sales", "how many units"]):
        # If a specific product is mentioned ("how many units of Product X"), 
        # it is a specific performance query, not a general "top 5" list.
        if entities["product"]:
             return {
                 "intent": "sales", 
                 "detail": "product_performance", 
                 "entities": entities
             }
        return {
            "intent": "sales", 
            "detail": "top_products", 
            "entities": entities
        }
    
    # Customer Intent
    if any(k in q for k in ["customer", "repeat", "repeat orders", "returning customers", "loyal"]):
        return {
            "intent": "customers", 
            "detail": "repeat_customers", 
            "entities": entities
        }
    
    # Fallback for future/forecast questions regarding specific products
    if any(k in q for k in ["next month", "future", "forecast", "predict"]):
        return {
            "intent": "inventory", 
            "detail": "inventory_projection", 
            "assumption": "based_on_past_sales",
            "entities": entities
        }
    
    # Fallback
    return {"intent": "unknown", "detail": "unknown", "entities": entities}