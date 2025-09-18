---
id: tracker-api
slug: /api/tracker
title: Expense Tracker API
sidebar_label: Expense Tracker
---

# Expense Tracker API

This section documents the endpoints for managing categories and transactions in the Expense Tracker API.

## Category Endpoints

### Create Category
**POST** `/tracker/categories`

Create a new category for the authenticated user.

#### Request Body
```json
{
  "name": "string"
}
```

#### Responses
- **200 OK**: Category created.
  ```json
  { "id": "uuid", "name": "string" }
  ```
- **400 Bad Request**: Category already exists.
  ```json
  { "detail": "Category already exists" }
  ```

---

### Update Category
**PUT** `/tracker/categories/{category_id}`

Update the name of an existing category.

#### Request Body
```json
{
  "name": "string"
}
```

#### Responses
- **200 OK**: Category updated.
  ```json
  { "id": "uuid", "name": "string" }
  ```
- **404 Not Found**: Category not found.
  ```json
  { "detail": "Category not found" }
  ```

---

### Delete Category
**DELETE** `/tracker/categories/{category_id}`

Delete a category and all related transactions for the authenticated user.

#### Responses
- **200 OK**: Category and related transactions deleted.
  ```json
  { "detail": "Category and N related transactions deleted" }
  ```
- **404 Not Found**: Category not found.
  ```json
  { "detail": "Category not found" }
  ```
- **400 Bad Request**: Invalid category ID.
  ```json
  { "detail": "Invalid category ID" }
  ```

---

### List Categories
**GET** `/tracker/categories`

List all categories for the authenticated user.

#### Responses
- **200 OK**: Array of categories.
  ```json
  [
    { "id": "uuid", "name": "string" },
    ...
  ]
  ```

---

## Transaction Endpoints

### Create Transaction
**POST** `/tracker/transactions`

Create a new transaction for the authenticated user.

#### Request Body
```json
{
  "title": "string",
  "amount": 0.0,
  "date": "2025-09-18T12:34:56.789Z",
  "category_ids": ["uuid1", "uuid2"]
}
```

#### Responses
- **200 OK**: Transaction created.
  ```json
  {
    "id": "uuid",
    "title": "string",
    "amount": 0.0,
    "date": "2025-09-18",
    "categories": [ { "id": "uuid", "name": "string" } ]
  }
  ```
- **400 Bad Request**: Invalid categories.
  ```json
  { "detail": "Invalid categories" }
  ```

---

### List Transactions
**GET** `/tracker/transactions`

List all transactions for the authenticated user.

#### Responses
- **200 OK**: Array of transactions.
  ```json
  [
    {
      "id": "uuid",
      "title": "string",
      "amount": 0.0,
      "date": "2025-09-18",
      "categories": [ { "id": "uuid", "name": "string" } ]
    },
    ...
  ]
  ```

---

### Update Transaction
**PATCH** `/tracker/transactions/{transaction_id}`

Update fields of an existing transaction.

#### Request Body
```json
{
  "title": "string",
  "amount": 0.0,
  "date": "2025-09-18T12:34:56.789Z",
  "category_ids": ["uuid1", "uuid2"]
}
```

#### Responses
- **200 OK**: Transaction updated.
  ```json
  {
    "id": "uuid",
    "title": "string",
    "amount": 0.0,
    "date": "2025-09-18",
    "categories": [ { "id": "uuid", "name": "string" } ]
  }
  ```
- **404 Not Found**: Transaction not found.
  ```json
  { "detail": "Transaction not found" }
  ```
- **400 Bad Request**: Invalid categories.
  ```json
  { "detail": "Invalid categories" }
  ```

---

### Delete Transaction
**DELETE** `/tracker/transactions/{transaction_id}`

Delete a transaction for the authenticated user.

#### Responses
- **200 OK**: Transaction deleted.
  ```json
  { "detail": "Transaction deleted" }
  ```
- **404 Not Found**: Transaction not found.
  ```json
  { "detail": "Transaction not found" }
  ```

---

## Models

### CategoryCreate
| Field | Type   | Description         |
|-------|--------|---------------------|
| name  | string | Category name (1-50 chars) |

### CategoryResponse
| Field | Type | Description      |
|-------|------|------------------|
| id    | uuid | Category ID      |
| name  | string | Category name   |

### TransactionCreate
| Field        | Type     | Description                |
|--------------|----------|----------------------------|
| title        | string   | Transaction title (1-100 chars) |
| amount       | float    | Transaction amount          |
| date         | string   | Transaction date (optional) |
| category_ids | uuid[]   | List of category IDs        |

### TransactionResponse
| Field      | Type   | Description         |
|------------|--------|---------------------|
| id         | uuid   | Transaction ID      |
| title      | string | Transaction title   |
| amount     | float  | Transaction amount  |
| date       | string | Transaction date    |
| categories | array  | List of categories  |

### TransactionUpdate
| Field        | Type     | Description                |
|--------------|----------|----------------------------|
| title        | string   | Transaction title (optional) |
| amount       | float    | Transaction amount (optional) |
| date         | string   | Transaction date (optional) |
| category_ids | uuid[]   | List of category IDs (optional) |
