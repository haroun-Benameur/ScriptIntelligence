# Rapport de génération des tests

**Date:** 2026-02-12T10:09:32.499305
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order Success

- **Description:** Verify that an order is successfully created when the user exists and quantity is positive.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Laptop', 'quantity': 1}`
- **Expected output:** JSON containing order_id, user_email: 'john.doe@example.com', product_name: 'Laptop', quantity: 1

### Test 2: Create Order User Not Found

- **Description:** Verify that a ValueError is raised when creating an order for a user email that does not exist in the system.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Laptop', 'quantity': 1}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total Success

- **Description:** Verify that the total price is correctly calculated based on unit_price and a quantity greater than 10.
- **Inputs:** `{'unit_price': 50.0, 'quantity': 11}`
- **Expected output:** 550.0

---

## Module: REQ-USER-001

### Test 1: Create User Success

- **Description:** Verify that a new user can be created with a unique name and email.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing id, name: 'John Doe', email: 'john.doe@example.com'

### Test 2: Create User Duplicate Email

- **Description:** Verify that a ValueError is raised when attempting to create a user with an email that already exists.
- **Inputs:** `{'name': 'Jane Smith', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email Success

- **Description:** Verify that the system returns user data when searching for a valid, existing email.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing user data for john.doe@example.com

### Test 2: Get User By Email Not Found

- **Description:** Verify that a ValueError is raised when the system searches for an email that does not exist.
- **Inputs:** `{'email': 'missing@example.com'}`
- **Expected output:** ValueError

---
