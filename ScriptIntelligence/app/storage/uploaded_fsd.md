# Functional Specification Document (FSD)

## Project: User & Order Management API

---

# 1. User Management

## REQ-USER-001: Create User

### Description
The system shall allow creation of a new user.

### Inputs
- name (string, required)
- email (string, required, unique)

### Expected Behavior
- If email does not exist → user is created
- If email already exists → raise ValueError

### Output
- JSON containing id, name, email

---

## REQ-USER-002: Get User By Email

### Description
The system shall return a user by email...

### Inputs
- email (string, required)

### Expected Behavior
- If user exists → return user data
- If not → raise ValueError

---

# 2. Order Management

## REQ-ORDER-001: Create Order

### Description
The system shall create an order linked to a user.

### Inputs
- user_email (string)
- product_name (string)
- quantity (int >1)

### Expected Behavior
- If user exists → create order
- If user does not exist → raise ValueError

### Output
- JSON containing order_id, user_email, product_name, quantity

---

## REQ-ORDER-002: Calculate Order Total

### Description
The system shall calculate total price.

### Inputs
- unit_price (float > 00)
- quantity (int > 0)

### Expected Behavior
- Return unit_price * quantity
