# Rapport de génération des tests

**Date:** 2026-02-12T10:12:53.591795
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order Success

- **Description:** Verify that an order is created successfully for an existing user with a quantity greater than 10.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Industrial Widget', 'quantity': 15}`
- **Expected output:** JSON containing order_id, user_email: 'john.doe@example.com', product_name: 'Industrial Widget', quantity: 15

### Test 2: Create Order Missing User Failure

- **Description:** Verify that a ValueError is raised when creating an order for an email that is not registered.
- **Inputs:** `{'user_email': 'nonexistent@example.com', 'product_name': 'Industrial Widget', 'quantity': 15}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total Success

- **Description:** Verify that the total price is correctly calculated as unit_price multiplied by quantity.
- **Inputs:** `{'unit_price': 25.5, 'quantity': 20}`
- **Expected output:** 510.0

---

## Module: REQ-USER-001

### Test 1: Create User Success

- **Description:** Verify that a new user is successfully created when provided with a unique email and name.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON object with unique id, name: 'John Doe', email: 'john.doe@example.com'

### Test 2: Create User Duplicate Email Failure

- **Description:** Verify that the system raises a ValueError when attempting to create a user with an email that already exists.
- **Inputs:** `{'name': 'Duplicate User', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email Success

- **Description:** Verify that the system returns user data for a valid existing email.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** User data containing id, name, and email: 'john.doe@example.com'

### Test 2: Get User By Email Not Found

- **Description:** Verify that a ValueError is raised when attempting to fetch a user with an email that does not exist.
- **Inputs:** `{'email': 'missing@example.com'}`
- **Expected output:** ValueError

---
