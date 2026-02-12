# Rapport de génération des tests

**Date:** 2026-02-12T14:31:24.751667
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify an order is created successfully when linked to an existing user email.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Laptop', 'quantity': 2}`
- **Expected output:** JSON containing order_id, user_email, product_name, and quantity.

### Test 2: Create Order - User Not Found

- **Description:** Verify that an order cannot be created if the user_email does not exist.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Monitor', 'quantity': 5}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Success

- **Description:** Verify the total price calculation for valid unit_price and quantity (> 10).
- **Inputs:** `{'unit_price': 50.0, 'quantity': 12}`
- **Expected output:** 600.0

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a new user is created successfully when the email does not exist.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing id, name, and email of the created user.

### Test 2: Create User - Duplicate Email

- **Description:** Verify that the system raises a ValueError when attempting to create a user with an existing email.
- **Inputs:** `{'name': 'Jane Smith', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError: Email already exists

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that user data is returned when a valid registered email is provided.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing user data (id, name, email).

### Test 2: Get User By Email - Not Found

- **Description:** Verify that the system raises a ValueError when the email does not exist in the system.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
