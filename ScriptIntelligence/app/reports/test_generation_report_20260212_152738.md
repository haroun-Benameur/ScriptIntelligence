# Rapport de génération des tests

**Date:** 2026-02-12T15:27:38.929968
**Total tests:** 8
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Valid User

- **Description:** Ensure an order is created successfully when linked to an existing user email.
- **Inputs:** `{'user_email': 'alice@example.com', 'product_name': 'Laptop', 'quantity': 1}`
- **Expected output:** JSON containing order_id, user_email 'alice@example.com', product_name 'Laptop', and quantity 1.

### Test 2: Create Order - Non-Existent User

- **Description:** Ensure the system raises a ValueError when trying to create an order for a user email that does not exist.
- **Inputs:** `{'user_email': 'ghost@example.com', 'product_name': 'Laptop', 'quantity': 1}`
- **Expected output:** Raise ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Valid

- **Description:** Ensure the total price is correctly calculated for quantities greater than 10.
- **Inputs:** `{'unit_price': 50.0, 'quantity': 12}`
- **Expected output:** 600.0

### Test 2: Calculate Order Total - Boundary Condition

- **Description:** Verify calculation works at the minimum required quantity threshold (e.g., 11).
- **Inputs:** `{'unit_price': 10.0, 'quantity': 11}`
- **Expected output:** 110.0

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Ensure a user can be successfully created when the email does not exist.
- **Inputs:** `{'name': 'Alice Smith', 'email': 'alice@example.com'}`
- **Expected output:** JSON containing a unique id, name 'Alice Smith', and email 'alice@example.com'.

### Test 2: Create User - Duplicate Email

- **Description:** Ensure the system raises a ValueError when attempting to create a user with an existing email.
- **Inputs:** `{'name': 'Alice Jones', 'email': 'alice@example.com'}`
- **Expected output:** Raise ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Ensure user data is returned when a valid, existing email is provided.
- **Inputs:** `{'email': 'alice@example.com'}`
- **Expected output:** User data matching the email 'alice@example.com'.

### Test 2: Get User By Email - Not Found

- **Description:** Ensure the system raises a ValueError when the email does not exist in the database.
- **Inputs:** `{'email': 'unknown@example.com'}`
- **Expected output:** Raise ValueError

---
