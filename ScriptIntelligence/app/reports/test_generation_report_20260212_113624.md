# Rapport de génération des tests

**Date:** 2026-02-12T11:36:24.449118
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create order for valid user

- **Description:** Ensure an order is successfully created when linked to an existing user email.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Laptop', 'quantity': 1}`
- **Expected output:** JSON containing order_id, user_email: 'john.doe@example.com', product_name: 'Laptop', quantity: 1

### Test 2: Create order for non-existent user

- **Description:** Ensure the system raises a ValueError when creating an order for a user email that does not exist.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Phone', 'quantity': 1}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate order total valid inputs

- **Description:** Ensure the system correctly calculates unit_price * quantity for valid input ranges.
- **Inputs:** `{'unit_price': 50.0, 'quantity': 15}`
- **Expected output:** 750.0

---

## Module: REQ-USER-001

### Test 1: Create valid user

- **Description:** Ensure a new user can be created when the email is unique.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing generated id, name: 'John Doe', email: 'john.doe@example.com'

### Test 2: Create user with duplicate email

- **Description:** Ensure the system raises a ValueError when attempting to create a user with an existing email.
- **Inputs:** `{'name': 'Jane Smith', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get user by existing email

- **Description:** Ensure user data is returned when a valid, existing email is provided.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** User object with name 'John Doe' and email 'john.doe@example.com'

### Test 2: Get user by non-existent email

- **Description:** Ensure the system raises a ValueError when the email does not exist in the system.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
