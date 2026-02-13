# Rapport de génération des tests

**Date:** 2026-02-12T16:02:11.377536
**Total tests:** 11
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order can be created for an existing user.
- **Inputs:** `{'user_email': 'jane.doe@example.com', 'product_name': 'Widget A', 'quantity': 5}`
- **Expected output:** JSON containing order_id, user_email: 'jane.doe@example.com', product_name: 'Widget A', quantity: 5

### Test 2: Create Order - User Missing

- **Description:** Verify that a ValueError is raised if the user_email provided does not exist.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Widget A', 'quantity': 1}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Total - Valid Positive Inputs

- **Description:** Verify that the total price is correctly calculated by multiplying unit price and quantity with standard positive values.
- **Inputs:** `{'unit_price': 10.5, 'quantity': 3}`
- **Expected output:** 31.5

### Test 2: Calculate Total - Decimal Precision

- **Description:** Verify calculation remains accurate with specific decimal unit prices (e.g., retail pricing).
- **Inputs:** `{'unit_price': 19.99, 'quantity': 2}`
- **Expected output:** 39.98

### Test 3: Calculate Total - Minimum Boundary

- **Description:** Verify the calculation with the lowest valid unit price and quantity.
- **Inputs:** `{'unit_price': 0.01, 'quantity': 1}`
- **Expected output:** 0.01

### Test 4: Calculate Total - Invalid Zero Quantity

- **Description:** Verify system behavior when quantity is 0 (violating quantity > 0 constraint).
- **Inputs:** `{'unit_price': 100.0, 'quantity': 0}`
- **Expected output:** ValueError or validation error indicating quantity must be greater than 0.

### Test 5: Calculate Total - Invalid Negative Unit Price

- **Description:** Verify system behavior when unit_price is 0 or less (violating unit_price > 0 constraint).
- **Inputs:** `{'unit_price': -5.0, 'quantity': 10}`
- **Expected output:** ValueError or validation error indicating unit_price must be greater than 0.

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a new user is created successfully when a unique email is provided.
- **Inputs:** `{'name': 'Jane Doe', 'email': 'jane.doe@example.com'}`
- **Expected output:** JSON containing generated id, name: 'Jane Doe', email: 'jane.doe@example.com'

### Test 2: Create User - Duplicate Email

- **Description:** Verify that a ValueError is raised when attempting to create a user with an email that already exists.
- **Inputs:** `{'name': 'Jane Smith', 'email': 'jane.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that user data is returned when a valid existing email is provided.
- **Inputs:** `{'email': 'jane.doe@example.com'}`
- **Expected output:** JSON containing user data (id, name, email)

### Test 2: Get User By Email - Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist in the system.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
