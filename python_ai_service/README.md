# Python AI Service — Shopify Analytics Agent (FastAPI)

## Overview

This service implements the **core AI analytics agent** for the Shopify AI Analytics assignment.
It receives a natural-language business question, determines user intent, generates a corresponding **ShopifyQL** query, processes the data (mocked for this assignment), and returns a **clear, business-friendly answer**.

The service is intentionally designed to demonstrate:

* Agentic reasoning and planning
* ShopifyQL generation and validation
* Practical handling of ambiguous or incomplete questions
* Explainable analytics instead of raw metrics

All Shopify API calls and OAuth are **mocked by design**, as permitted by the assignment, to focus on reasoning clarity and architecture.

---

## API Endpoint

### `POST /ask`

**Request Body**

```json
{
  "store_id": "demo.myshopify.com",
  "question": "How much inventory should I reorder for next week?"
}
```

**Response Body**

```json
{
  "answer": "Inventory recommendation (next 7 days with 20% safety):\nClassic Latte Mug: avg 10/day → reorder 84 units",
  "confidence": "medium",
  "debug": {
    "shopifyql": "...",
    "intent": {
      "intent": "inventory",
      "detail": "inventory_projection"
    }
  }
}
```

### Response Fields

* **answer** → Plain-English business explanation
* **confidence** → Reliability indicator (`low | medium | high`)
* **debug** → Internal reasoning details (for review & debugging)

---

## Project Structure

```
python_ai_service/
├── app/
│   ├── main.py                  # FastAPI app and request orchestration
│   ├── schemas.py               # Request/response schemas
│   └── agent/
│       ├── intent_classifier.py # Intent detection & ambiguity handling
│       ├── shopifyql_generator.py # ShopifyQL generation & validation
│       ├── data_fetcher.py      # Mocked Shopify data access
│       └── explainer.py         # Business-friendly explanation logic
└── requirements.txt
```

Each module has a **single responsibility**, making the agent easy to reason about, test, and extend.

---

## How to Run (Local)

### Prerequisites

* Python **3.10+**
* pip
* curl or Postman

### Steps

```bash
cd python_ai_service
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Git Bash / WSL
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Service will be available at:

```
http://localhost:8000
```

> ⚠️ Important:
> Always run `uvicorn` from the **python_ai_service** directory so that package imports work correctly.

---

## Agent Workflow (Detailed)

The AI agent follows a deterministic and explainable workflow:

1. **Intent Classification**
   (`intent_classifier.py`)
   Determines whether the question relates to:

   * Sales
   * Inventory
   * Customers
     Ambiguous future-oriented questions explicitly carry assumptions.

2. **ShopifyQL Generation**
   (`shopifyql_generator.py`)
   Builds a ShopifyQL query template appropriate for the detected intent and time range.

3. **Query Validation**
   Ensures generated ShopifyQL is syntactically valid before execution.

4. **Data Retrieval (Mocked)**
   (`data_fetcher.py`)
   Returns realistic sample datasets aligned with the query type.

5. **Explanation Layer**
   (`explainer.py`)
   Converts technical metrics into clear business insights such as:

   * Daily averages
   * Reorder quantities
   * Top-selling products

---

## Example Test (curl)

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"store_id":"demo.myshopify.com","question":"What were my top 5 selling products last week?"}'
```

**Expected Output**

```json
{
  "answer": "Top selling products in the last 7 days:\n1. Classic Latte Mug — 120 units\n2. Retro Coffee Beans 1kg — 95 units",
  "confidence": "high",
  "debug": {
    "shopifyql": "SELECT product_title, SUM(quantity) AS total_sold FROM orders WHERE created_at >= -7d GROUP BY product_title ORDER BY total_sold DESC LIMIT 5",
    "intent": {
      "intent": "sales",
      "detail": "top_products"
    }
  }
}
```

---

## Handling Real-World Data Issues

* Ambiguous timeframes are resolved using reasonable defaults.
* Empty or missing data returns safe, user-friendly fallback responses.
* Query validation prevents unsafe or malformed analytics queries.
* Confidence scores communicate uncertainty clearly to the user.

---

## Notes & Production Enhancements

To make this service production-ready:

* Replace mocked data fetcher with live Shopify Admin API calls
* Implement Shopify OAuth token management
* Use an LLM for richer intent and entity extraction
* Add caching for repeated analytics queries
* Log agent decisions for observability and debugging

These features are intentionally scoped out to prioritize agent reasoning and clarity for this assignment.

---

## Summary

* This service contains **all AI and analytics logic**
* Designed for clarity, explainability, and maintainability
* Fully aligned with the assignment’s agentic workflow expectations
* Mocked integrations are explicit, justified, and replaceable

