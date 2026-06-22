# CodeVector Backend Assignment

## Overview

This project is a FastAPI backend that allows users to browse a catalog of 200,000 products with support for:

* Product listing
* Category filtering
* Cursor-based pagination
* PostgreSQL storage
* Efficient querying using database indexes

The API is designed to handle large datasets efficiently and provide correct pagination even when products are added or updated while users are browsing.

---

## Tech Stack

* FastAPI
* PostgreSQL (Neon)
* SQLAlchemy
* Python

---

## Database Schema

Each product contains:

* id (unique identifier)
* name
* category
* price
* created_at
* updated_at

---

## Data Generation

A seed script (`seed.py`) is included to generate and insert 200,000 products into the database.

To improve insertion performance, records are inserted in batches using bulk operations instead of inserting rows one by one.

---

## Pagination Approach

### Why Not Offset Pagination?

Offset pagination can lead to duplicate or missing records when new products are inserted or updated while a user is browsing.

Example:

1. User loads page 1.
2. New products are added.
3. User requests page 2.
4. Some products may be skipped or repeated because row positions have shifted.

### Cursor Pagination

To solve this problem, cursor-based pagination is used.

Products are ordered by:

```sql
updated_at DESC,
id DESC
```

The API returns a cursor containing:

```json
{
  "cursor_time": "...",
  "cursor_id": ...
}
```

The next request uses this cursor to fetch products after the last product from the previous page.

This ensures users do not see duplicate products or miss products while data is changing.

---

## Database Indexes

The following indexes are used to keep pagination and filtering fast:

```sql
CREATE INDEX idx_products_updated_id
ON products(updated_at DESC, id DESC);

CREATE INDEX idx_products_category_updated_id
ON products(category, updated_at DESC, id DESC);
```

These indexes support:

* Fast cursor pagination
* Fast category filtering
* Efficient queries on large datasets

---

## API Endpoints

### Health Check

```http
GET /
```

Response:

```json
{
  "message": "Hello FastAPI"
}
```

---

### Get Products

```http
GET /products
```

Query Parameters:

| Parameter   | Description                  |
| ----------- | ---------------------------- |
| limit       | Number of products to return |
| category    | Filter by category           |
| cursor_time | Pagination cursor timestamp  |
| cursor_id   | Pagination cursor id         |

Example:

```http
GET /products?limit=20
```

```http
GET /products?category=Electronics
```

```http
GET /products?cursor_time=2026-06-22T10:15:00&cursor_id=12345
```

---

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables:

```env
DATABASE_URL=<your_postgresql_connection_string>
```

Run the server:

```bash
uvicorn main:app --reload
```

---

## Future Improvements

Given more time, I would:

* Add automated tests
* Add Alembic migrations
* Add Pydantic response models
* Add caching for frequently accessed queries
* Add monitoring and logging
* Add API rate limiting

---

## AI Usage

AI tools were used to speed up development, discuss architecture options, and review implementation approaches.

All generated code and design decisions were manually reviewed, tested, and adapted to satisfy the assignment requirements, particularly around cursor pagination, indexing, and performance considerations.
