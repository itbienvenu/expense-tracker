---
id: authentication-api
slug: /api/authentication
title: Authentication API
sidebar_label: Authentication
---

# Authentication API

This section describes the authentication endpoints for the Expense Tracker API. These endpoints allow users to register, log in, and retrieve their profile information.

## Register a New User

**POST** `/auth/register`

Registers a new user account.

### Request Body
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

### Responses
- **200 OK**: User created successfully or password strength errors.
  ```json
  { "detail": "User created well" }
  ```
- **400 Bad Request**: Email already registered.
  ```json
  { "detail": "Email already registered" }
  ```

---

## User Login

**POST** `/auth/login`

Authenticates a user and returns a JWT access token.

### Request Body
```json
{
  "email": "user@example.com",
  "hashed_password": "string"
}
```

### Responses
- **200 OK**: Login successful.
  ```json
  { "access_token": "jwt-token", "token_type": "bearer" }
  ```
- **401 Unauthorized**: Invalid email or password.
  ```json
  { "detail": "Invalid email or password" }
  ```

---

## Get Current User Info

**GET** `/auth/me`

Returns information about the currently authenticated user (requires JWT token).

### Headers
- `Authorization: Bearer <access_token>`

### Response
- **200 OK**:
  ```json
  {
    "id": "uuid",
    "username": "string",
    "email": "user@example.com",
    "created_at": "2025-09-18T12:34:56.789Z"
  }
  ```
- **401 Unauthorized**: Invalid or missing token.
  ```json
  { "detail": "Invalid user ID format" }
  ```

---

## Models

### UserRegister
| Field    | Type   | Description         |
|----------|--------|---------------------|
| username | string | User's username     |
| email    | string | User's email        |
| password | string | User's password     |

### UserLogin
| Field           | Type   | Description         |
|-----------------|--------|---------------------|
| email           | string | User's email        |
| hashed_password | string | User's password     |

### UserInfoResponse
| Field      | Type   | Description         |
|------------|--------|---------------------|
| id         | uuid   | User's unique ID    |
| username   | string | User's username     |
| email      | string | User's email        |
| created_at | string | Account created at  |
