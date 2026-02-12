# Rapport de génération des tests

**Date:** 2026-02-12T09:53:02.694336
**Total tests:** 8
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order is successfully created for an existing user with valid product and quantity.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Laptop', 'quantity': 1}`
- **Expected output:** JSON containing order_id, user_email: 'john.doe@example.com', product_name: 'Laptop', quantity: 1

### Test 2: Create Order - User Not Found

- **Description:** Verify that a ValueError is raised when attempting to create an order for a user email that does not exist.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Laptop', 'quantity': 1}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Standard Calculation

- **Description:** Verify the calculation logic returns unit_price multiplied by quantity.
- **Inputs:** `{'unit_price': 99.99, 'quantity': 11}`
- **Expected output:** 1099.89

### Test 2: Calculate Order Total - Invalid Quantity

- **Description:** Verify the behavior when quantity is outside the specified range (> 10).
- **Inputs:** `{'unit_price': 50.0, 'quantity': 5}`
- **Expected output:** Error or unexpected behavior based on boundary constraints

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a user is successfully created when providing a unique email and a name.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing id, name: 'John Doe', email: 'john.doe@example.com'

### Test 2: Create User - Duplicate Email

- **Description:** Verify that a ValueError is raised when attempting to create a user with an email that already exists in the system.
- **Inputs:** `{'name': 'Jane Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that the system returns the correct user data when a valid, existing email is provided.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing user data for john.doe@example.com

### Test 2: Get User By Email - Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist in the system.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
