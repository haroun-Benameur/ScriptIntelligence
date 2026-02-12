# Rapport de génération des tests

**Date:** 2026-02-12T09:57:03.435064
**Total tests:** 8
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order Success

- **Description:** Verify that an order is successfully created when linked to an existing user email.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Wireless Mouse', 'quantity': 2}`
- **Expected output:** JSON containing order_id, user_email, product_name, and quantity.

### Test 2: Create Order User Not Found

- **Description:** Verify that creating an order for a non-existent user email raises a ValueError.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Keyboard', 'quantity': 1}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total Calculation

- **Description:** Verify that the total price is correctly calculated as unit_price multiplied by quantity.
- **Inputs:** `{'unit_price': 25.5, 'quantity': 12}`
- **Expected output:** 306.0

### Test 2: Calculate Order Total Minimum Constraints

- **Description:** Verify calculation logic using minimum valid quantity according to specification (>10).
- **Inputs:** `{'unit_price': 10.0, 'quantity': 11}`
- **Expected output:** 110.0

---

## Module: REQ-USER-001

### Test 1: Create User Successfully

- **Description:** Verify that a user can be created with a valid name and a unique email.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing generated id, name: 'John Doe', email: 'john.doe@example.com'

### Test 2: Create User Duplicate Email

- **Description:** Verify that creating a user with an email that already exists raises a ValueError.
- **Inputs:** `{'name': 'Jane Smith', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email Success

- **Description:** Verify that user data is returned when a valid, existing email is provided.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** User data matching the email provided.

### Test 2: Get User By Email Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist in the system.
- **Inputs:** `{'email': 'missing@example.com'}`
- **Expected output:** ValueError

---
