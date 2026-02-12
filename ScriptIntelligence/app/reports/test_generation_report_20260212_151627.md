# Rapport de génération des tests

**Date:** 2026-02-12T15:16:27.474812
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order Success

- **Description:** Verify that an order is successfully created and linked when the user_email exists.
- **Inputs:** `{'user_email': 'alice@example.com', 'product_name': 'Widget A', 'quantity': 5}`
- **Expected output:** JSON containing order_id, user_email: 'alice@example.com', product_name: 'Widget A', quantity: 5

### Test 2: Create Order User Not Found

- **Description:** Verify that a ValueError is raised when trying to create an order for a user email that does not exist.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Widget A', 'quantity': 5}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total Valid

- **Description:** Verify that the total price is correctly calculated as unit_price * quantity.
- **Inputs:** `{'unit_price': 15.0, 'quantity': 20}`
- **Expected output:** 300.0

---

## Module: REQ-USER-001

### Test 1: Create New User Success

- **Description:** Verify that a user is successfully created when providing a unique email and name.
- **Inputs:** `{'name': 'Alice Smith', 'email': 'alice@example.com'}`
- **Expected output:** JSON containing id, name: 'Alice Smith', email: 'alice@example.com'

### Test 2: Create User Duplicate Email

- **Description:** Verify that a ValueError is raised when attempting to create a user with an email that already exists in the system.
- **Inputs:** `{'name': 'Alice Duplicate', 'email': 'alice@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get Existing User By Email

- **Description:** Verify that the system returns the correct user data when a valid, existing email is provided.
- **Inputs:** `{'email': 'alice@example.com'}`
- **Expected output:** User object containing id, name, and email: 'alice@example.com'

### Test 2: Get User By Email Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist in the system.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
