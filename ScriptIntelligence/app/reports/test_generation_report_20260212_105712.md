# Rapport de génération des tests

**Date:** 2026-02-12T10:57:12.245944
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order is created successfully if the user email exists.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Wireless Mouse', 'quantity': 2}`
- **Expected output:** JSON object containing order_id, user_email, product_name, and quantity.

### Test 2: Create Order - Missing User

- **Description:** Verify that creating an order for a non-existent user raises a ValueError.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Monitor', 'quantity': 1}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Success

- **Description:** Verify that the system correctly calculates total price (unit_price * quantity).
- **Inputs:** `{'unit_price': 50.0, 'quantity': 12}`
- **Expected output:** 600.0

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a user can be successfully created with a unique email.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** A JSON object containing id, name, and email.

### Test 2: Create User - Duplicate Email Error

- **Description:** Verify that creating a user with an already existing email raises a ValueError.
- **Inputs:** `{'name': 'Jane Smith', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that user data is returned when searching for an existing email.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** JSON object with user data (id, name, email).

### Test 2: Get User By Email - Not Found

- **Description:** Verify that searching for a non-existent email raises a ValueError.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
