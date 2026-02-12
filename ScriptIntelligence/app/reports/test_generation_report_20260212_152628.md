# Rapport de génération des tests

**Date:** 2026-02-12T15:26:28.031191
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order is created successfully when the user exists and quantity > 1.
- **Inputs:** `{'user_email': 'alice@example.com', 'product_name': 'Mechanical Keyboard', 'quantity': 2}`
- **Expected output:** JSON object containing order_id, user_email, product_name, quantity

### Test 2: Create Order - User Not Found

- **Description:** Verify that an order cannot be created for a user email that does not exist in the system.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Mouse Pad', 'quantity': 5}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Success

- **Description:** Verify that the total price is calculated as unit_price multiplied by quantity.
- **Inputs:** `{'unit_price': 15.5, 'quantity': 12}`
- **Expected output:** 186.0

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a new user is successfully created when a unique email is provided.
- **Inputs:** `{'name': 'Alice Smith', 'email': 'alice@example.com'}`
- **Expected output:** JSON object with id, name='Alice Smith', email='alice@example.com'

### Test 2: Create User - Duplicate Email

- **Description:** Verify that creating a user with an already existing email raises a ValueError.
- **Inputs:** `{'name': 'Alice Duplicate', 'email': 'alice@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that user data is returned when searching for an existing email.
- **Inputs:** `{'email': 'alice@example.com'}`
- **Expected output:** User data object matching alice@example.com

### Test 2: Get User By Email - Not Found

- **Description:** Verify that searching for a non-existent email raises a ValueError.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
