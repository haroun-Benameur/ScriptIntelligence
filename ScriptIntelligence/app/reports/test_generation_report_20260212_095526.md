# Rapport de génération des tests

**Date:** 2026-02-12T09:55:26.938661
**Total tests:** 8
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order is created successfully for an existing user.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Laptop', 'quantity': 1}`
- **Expected output:** JSON containing order_id, user_email: 'john.doe@example.com', product_name: 'Laptop', quantity: 1

### Test 2: Create Order - Missing User

- **Description:** Verify that a ValueError is raised when creating an order for a user email that does not exist.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Mouse', 'quantity': 2}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Standard Calculation

- **Description:** Verify that the total price is correctly calculated as unit_price * quantity.
- **Inputs:** `{'unit_price': 15.5, 'quantity': 12}`
- **Expected output:** 186.0

### Test 2: Calculate Order Total - Minimum Valid Quantity

- **Description:** Verify calculation when quantity is just above the threshold (>10).
- **Inputs:** `{'unit_price': 10.0, 'quantity': 11}`
- **Expected output:** 110.0

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a new user is created successfully when the email is unique.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing generated id, name: 'John Doe', email: 'john.doe@example.com'

### Test 2: Create User - Duplicate Email

- **Description:** Verify that a ValueError is raised when attempting to create a user with an existing email.
- **Inputs:** `{'name': 'Jane Smith', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that user data is returned correctly when a valid email is provided.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** User data object matching the email provided.

### Test 2: Get User By Email - Not Found

- **Description:** Verify that a ValueError is raised when the provided email does not exist in the system.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
