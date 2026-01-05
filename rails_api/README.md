# Rails API — Backend Gateway

## Overview

This Rails application serves as a **thin backend gateway** between clients and the Python AI service.
Its responsibility is intentionally limited to **request validation, routing, and response forwarding**, ensuring a clean separation of concerns.

All **AI reasoning, ShopifyQL generation, and analytics logic live exclusively in the Python service**.

---

## Responsibilities

The Rails API performs the following tasks:

* Accepts natural-language analytics questions from clients
* Validates required input fields
* Forwards requests to the Python AI service
* Returns the AI service response transparently
* Acts as the single backend entry point for clients

The Rails app **does not**:

* Contain business logic
* Generate ShopifyQL
* Perform data analysis
* Call Shopify APIs directly

This design aligns with the assignment’s architecture expectations.

---

## API Endpoint

### `POST /api/v1/questions`

**Request Body**

```json
{
  "store_id": "example-store.myshopify.com",
  "question": "How much inventory should I reorder for next week?"
}
```

**Behavior**

* Validates presence of `store_id` and `question`
* Forwards payload to the Python AI service at:

  ```
  http://localhost:8000/ask
  ```
* Returns the Python service response **unchanged**, including HTTP status codes

---

## Example Request

```bash
curl -X POST http://127.0.0.1:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{"store_id":"demo.myshopify.com","question":"What were my top 5 selling products last week?"}'
```

**Example Response**

```json
{
  "answer": "Top selling products in the last 7 days:\n1. Classic Latte Mug — 120 units\n2. Retro Coffee Beans 1kg — 95 units",
  "confidence": "high",
  "debug": {
    "shopifyql": "...",
    "intent": { "intent": "sales", "detail": "top_products" }
  }
}
```

---

## Project Files of Interest

* `app/controllers/api/v1/questions_controller.rb`
  Handles input validation and forwards requests to the Python AI service.

* `config/routes.rb`
  Declares the API route.

---

## Running the Rails API (Optional)

If you have Ruby & Rails installed:

```bash
cd rails_api
bundle install
rails server -p 3000
```

Rails will run at:

```
http://localhost:3000
```

---

## Error Handling

* Missing parameters → `422 Unprocessable Entity`
* Python service unavailable → `500 Internal Server Error`
* All Python service errors are forwarded transparently

This ensures consistent error behavior across services.

---

## Security & Production Notes

For a production deployment, the following would be added:

* API authentication (API keys / JWT)
* Secure Shopify OAuth token storage
* HTTPS and secure inter-service communication
* Request logging and rate limiting
* Circuit breakers for Python service failures

These are intentionally omitted here to keep the focus on architecture and agent reasoning, as requested by the assignment.

---

## Design Rationale

This gateway follows the **Backend-for-Frontend (BFF)** pattern:

* Rails = API gateway and orchestration
* Python = intelligence and analytics

This separation improves maintainability, testability, and scalability.

---

## Summary

* Rails API is **minimal by design**
* Clean separation of responsibilities
* Easy to replace or extend
* Fully aligned with assignment expectations

