# Shopify AI Analytics — Mini Assignment

## Overview

This repository contains a **mini AI-powered Shopify analytics system** built as part of an interview assignment.
The system allows users to ask **natural-language business questions** (sales, inventory, customers), converts them into **ShopifyQL**, processes the data, and returns **simple, business-friendly insights**.

The solution is intentionally designed to emphasize:

* **System architecture & separation of concerns**
* **Agent reasoning clarity**
* **Explainability over raw data**
* **Design correctness over production polish**

Live Shopify integration is **mocked by design**, as permitted by the assignment, to keep focus on reasoning and workflow clarity.

---

## Architecture at a Glance

```
Client / Postman
        |
        v
Rails API Gateway
(Validation, Routing)
        |
        v
Python AI Service (FastAPI)
(Intent → ShopifyQL → Data → Explanation)
```

* **Rails API** acts as a backend gateway.
* **Python AI Service** contains the agentic reasoning pipeline.
* **Shopify data & OAuth** are mocked, but ShopifyQL generation and validation are real.

---

## Project Structure

```
shopify-ai-analytics/
├── README.md                     # This file
├── architecture/
│   └── architecture_diagram.png
├── python_ai_service/             # AI Agent (FastAPI)
│   ├── README.md
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── schemas.py
│       └── agent/
│           ├── intent_classifier.py
│           ├── shopifyql_generator.py
│           ├── data_fetcher.py
│           └── explainer.py
└── rails_api/                     # Backend Gateway (Rails API)
    ├── README.md
    ├── Gemfile
    ├── app/controllers/api/v1/
    │   └── questions_controller.rb
    └── config/routes.rb
```

---

## How to Run (Local)

### Prerequisites

* Python **3.10+**
* pip
* (Optional) Ruby **3.2+** & Rails **7.x**
* curl or Postman

---

### Step 1: Run Python AI Service (Recommended First)

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

Service runs at:
👉 `http://localhost:8000`

---

### Step 2: (Optional) Run Rails API Gateway

```bash
cd rails_api
bundle install
rails server -p 3000
```

Rails runs at:
👉 `http://localhost:3000`

---

### Step 3: Test the API

**Via Rails (end-to-end):**

```bash
curl -X POST http://127.0.0.1:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{"store_id":"demo.myshopify.com","question":"How much inventory should I reorder for next week?"}'
```

**Directly via Python:**

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"store_id":"demo.myshopify.com","question":"What were my top 5 selling products last week?"}'
```

---

## Agent Workflow (Core Logic)

The agent follows a clear, deterministic workflow aligned with the assignment:

1. **Intent Interpretation**
   (`intent_classifier.py`)
   Detects whether the question relates to sales, inventory, or customers.

2. **Planning & ShopifyQL Generation**
   (`shopifyql_generator.py`)
   Builds a ShopifyQL query template based on intent and timeframe.

3. **Query Validation**
   Ensures the generated query is syntactically valid before execution.

4. **Data Retrieval**
   (`data_fetcher.py`)
   Returns realistic **mocked Shopify data** corresponding to the query.

5. **Explanation Layer**
   (`explainer.py`)
   Converts metrics into **plain-English business insights** with confidence levels.

---

## Sample Output

```json
{
  "answer": "Inventory recommendation (next 7 days with 20% safety):\nClassic Latte Mug: avg 10/day → reorder 84 units",
  "confidence": "medium",
  "debug": {
    "shopifyql": "SELECT product_id, product_title, SUM(quantity) AS total_sold_30d FROM orders WHERE created_at >= -30d GROUP BY product_id, product_title",
    "intent": { "intent": "inventory", "detail": "inventory_projection" }
  }
}
```

---

## Assumptions & Limitations

* Shopify OAuth and live API calls are **mocked intentionally** to focus on agent design.
* ShopifyQL is **generated and validated**, but not executed against a real store.
* Forecasting uses **historical averages**, not predictive ML models.
* Confidence scores (`low | medium | high`) indicate reliability based on assumptions.

---

## Production Considerations

To convert this prototype into a production system:

1. Implement Shopify OAuth and securely store access tokens.
2. Replace mocked data fetcher with Shopify Admin API calls.
3. Execute ShopifyQL against live store data.
4. Add caching, retries, and observability.
5. Store conversation context and logs in PostgreSQL.

---

## Submission Notes

This submission prioritizes:

* **Agent reasoning clarity**
* **Clean API design**
* **Readable, maintainable code**
* **Clear explanation of results**

Production integrations are intentionally scoped out and documented.

---

## Author

**Tamanna Bhrigunath**
Prepared for **Cafe Nostalgia / Internshala AI Analytics Assignment**

