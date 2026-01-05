from fastapi import FastAPI, HTTPException
from app.schemas import AskRequest, AskResponse
from app.agent.intent_classifier import classify_intent
from app.agent.shopifyql_generator import generate_shopifyql, validate_shopifyql
from app.agent.data_fetcher import fetch_shopify_data
from app.agent.explainer import explain

app = FastAPI(title="Shopify AI Analytics (mock)")

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    # 1. classify intent
    intent = classify_intent(req.question)

    # 2. generate shopifyql (informative)
    shopifyql = generate_shopifyql(intent, req.question)

    if not validate_shopifyql(shopifyql):
        raise HTTPException(status_code=400, detail="Invalid ShopifyQL generated")
    
    # 3. fetch data (mock / or real in future)
    raw_data = fetch_shopify_data(shopifyql, req.store_id)

    # 4. explain results
    result = explain(intent, raw_data, req.question)

    # Attach debug info (shopifyql) in debug field - helpful for reviewer
    debug = result.get("debug", {})
    debug["shopifyql"] = shopifyql
    debug["intent"] = intent

    return {
        "answer": result["answer"],
        "confidence": result["confidence"],
        "debug": debug
    }

