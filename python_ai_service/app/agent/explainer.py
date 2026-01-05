# Convert raw data into human-friendly explanation + confidence
def explain(intent_dict: dict, raw_data: dict, question: str) -> dict:
    intent = intent_dict.get("intent")

    if intent == "sales" and "top_products" in raw_data:
        items = raw_data["top_products"]
        lines = [f"{i+1}. {p['product_title']} — {p['total_sold']} units" for i,p in enumerate(items)]
        answer = "Top selling products in the last 7 days:\n" + "\n".join(lines)
        return {"answer": answer, "confidence": "high", "debug": {"period_days": raw_data.get("period_days")}}

    if intent == "inventory" and "sales_30d" in raw_data:
        # simple reorder logic: avg_daily = total_sold_30d / 30; reorder for 7 days lead + safety 20%
        recommendations = []
        for p in raw_data["sales_30d"]:
            total_30 = p["total_sold_30d"]
            avg_daily = total_30 / raw_data.get("period_days", 30)
            needed_next_7 = avg_daily * 7
            safety = needed_next_7 * 0.2
            reorder_qty = int(round(needed_next_7 + safety))
            recommendations.append({
                "product_title": p["product_title"],
                "avg_daily": round(avg_daily,2),
                "recommend_reorder_qty": reorder_qty
            })
        lines = [f"{r['product_title']}: avg {r['avg_daily']} /day → reorder {r['recommend_reorder_qty']} units" for r in recommendations]
        answer = "Inventory recommendation (next 7 days with 20% safety):\n" + "\n".join(lines)
        return {"answer": answer, "confidence": "medium", "debug": {"method": "avg30d*7 +20%"}}

    if intent == "customers" and "repeat_customers" in raw_data:
        custs = raw_data["repeat_customers"]
        answer = f"Found {len(custs)} customers with repeat orders in the last 90 days. Example IDs: " + ", ".join(str(c["customer_id"]) for c in custs[:5])
        return {"answer": answer, "confidence": "high", "debug": {"period_days": raw_data.get("period_days")}}

    # fallback
    return {"answer": "Sorry — I couldn't find enough data to answer that. Try a more specific question like 'top 5 products last 7 days' or 'how much to reorder for next 7 days'.", "confidence": "low", "debug": {}}
