# Rapport de génération des tests

**Date:** 2026-02-12T15:17:39.630747
**Total tests:** 9
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order is successfully created when a valid user email exists and quantity is greater than 1.
- **Inputs:** `{'user_email': 'existing_user@example.com', 'product_name': 'Laptop', 'quantity': 5}`
- **Expected output:** JSON containing order_id, user_email: 'existing_user@example.com', product_name: 'Laptop', quantity: 5

### Test 2: Create Order - User Not Found

- **Description:** Verify that the system raises a ValueError when the user_email provided does not exist in the system.
- **Inputs:** `{'user_email': 'non_existent@example.com', 'product_name': 'Monitor', 'quantity': 2}`
- **Expected output:** ValueError

### Test 3: Create Order - Invalid Quantity (Boundary)

- **Description:** Verify that an order is not created and raises a ValueError when quantity is 1 (violating the > 1 requirement).
- **Inputs:** `{'user_email': 'existing_user@example.com', 'product_name': 'Mouse', 'quantity': 1}`
- **Expected output:** ValueError

### Test 4: Create Order - Minimum Valid Quantity

- **Description:** Verify that an order is successfully created when the quantity is exactly 2.
- **Inputs:** `{'user_email': 'existing_user@example.com', 'product_name': 'Keyboard', 'quantity': 2}`
- **Expected output:** JSON containing order_id, user_email: 'existing_user@example.com', product_name: 'Keyboard', quantity: 2

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
