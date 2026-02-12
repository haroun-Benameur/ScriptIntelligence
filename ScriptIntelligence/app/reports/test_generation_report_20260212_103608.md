# Rapport de génération des tests

**Date:** 2026-02-12T10:36:08.064620
**Total tests:** 9
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order is successfully created for an existing user with a valid quantity.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Wireless Mouse', 'quantity': 2}`
- **Expected output:** JSON containing order_id, user_email 'john.doe@example.com', product_name 'Wireless Mouse', and quantity 2.

### Test 2: Create Order - Missing User

- **Description:** Verify that a ValueError is raised when attempting to create an order for a user email that does not exist.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Keyboard', 'quantity': 1}`
- **Expected output:** ValueError

### Test 3: Create Order - Invalid Quantity

- **Description:** Verify that an error is raised if the quantity is less than or equal to zero.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Monitor', 'quantity': 0}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Success

- **Description:** Verify that the total price is correctly calculated as unit_price * quantity for quantities greater than 10.
- **Inputs:** `{'unit_price': 15.5, 'quantity': 12}`
- **Expected output:** 186.0

### Test 2: Calculate Order Total - Constraint Check

- **Description:** Verify system behavior when quantity does not meet the requirement of being greater than 10.
- **Inputs:** `{'unit_price': 50.0, 'quantity': 5}`
- **Expected output:** System should fail validation or return error according to the quantity > 10 constraint.

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a user is created successfully when providing a unique name and email.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing a generated id, name 'John Doe', and email 'john.doe@example.com'.

### Test 2: Create User - Duplicate Email

- **Description:** Verify that the system raises a ValueError when attempting to create a user with an existing email.
- **Inputs:** `{'name': 'Jane Smith', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User - Success

- **Description:** Verify that user data is returned correctly when searching by an existing email.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing user data (id, name, email) for 'john.doe@example.com'.

### Test 2: Get User - Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist in the system.
- **Inputs:** `{'email': 'not.found@example.com'}`
- **Expected output:** ValueError

---
