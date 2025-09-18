---
id: reports-api
slug: /api/reports
title: Reports API
sidebar_label: Reports
---

# Reports API

This section documents the reports endpoint for filtering and retrieving transactions with various filters and sorting options.

## Get Filtered Transactions

**GET** `/reports/`

Retrieve transactions for the authenticated user, filtered and sorted by various criteria.

### Query Parameters
| Name         | Type     | Description                        |
|--------------|----------|------------------------------------|
| start_date   | string   | Filter from this date (YYYY-MM-DD) |
| end_date     | string   | Filter until this date (YYYY-MM-DD)|
| category_ids | uuid[]   | Filter by category IDs             |
| min_amount   | float    | Minimum transaction amount         |
| max_amount   | float    | Maximum transaction amount         |
| sort_by      | string   | Sort by: `date` or `amount`        |
| order        | string   | Order: `asc` or `desc`             |

### Example Request
```
GET /reports/?start_date=2025-09-01&end_date=2025-09-18&min_amount=10&max_amount=100&sort_by=amount&order=asc
```

### Responses
- **200 OK**: Array of filtered transactions.
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

### Notes
- All filters are optional. If omitted, all transactions for the user are returned.
- Requires authentication (JWT token).
- Sorting defaults to `date` descending.

---



