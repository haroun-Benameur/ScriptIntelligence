# Rapport de génération des tests

**Date:** 2026-02-13T14:06:03.222060
**Total tests:** 8
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order Success

- **Description:** Verify that an order is successfully created and linked when the user email exists.
- **Inputs:** `{'user_email': 'alice.smith@example.com', 'product_name': 'Wireless Mouse', 'quantity': 2}`
- **Expected output:** JSON containing order_id, user_email: 'alice.smith@example.com', product_name: 'Wireless Mouse', quantity: 2.

### Test 2: Create Order User Not Found

- **Description:** Verify that a ValueError is raised when creating an order for an email that is not registered in the system.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Keyboard', 'quantity': 1}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total Calculation

- **Description:** Verify that the system correctly calculates the total price based on unit_price and quantity.
- **Inputs:** `{'unit_price': 49.99, 'quantity': 3}`
- **Expected output:** 149.97

### Test 2: Calculate Order Total Boundary

- **Description:** Verify calculation with minimum valid values.
- **Inputs:** `{'unit_price': 0.01, 'quantity': 1}`
- **Expected output:** 0.01

---

## Module: REQ-USER-001

### Test 1: Create New User Success

- **Description:** Verify that a new user is successfully created when a unique email is provided.
- **Inputs:** `{'name': 'Alice Smith', 'email': 'alice.smith@example.com'}`
- **Expected output:** JSON containing a generated id, name: 'Alice Smith', and email: 'alice.smith@example.com'.

### Test 2: Create User Duplicate Email

- **Description:** Verify that a ValueError is raised when attempting to create a user with an email that already exists in the system.
- **Inputs:** `{'name': 'Alice Duplicate', 'email': 'alice.smith@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email Success

- **Description:** Verify that the system returns the correct user data when a valid, existing email is provided.
- **Inputs:** `{'email': 'alice.smith@example.com'}`
- **Expected output:** JSON object containing user details for alice.smith@example.com.

### Test 2: Get User By Email Not Found

- **Description:** Verify that the system raises a ValueError when attempting to retrieve a user using an email that does not exist.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
