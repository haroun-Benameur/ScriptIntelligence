# Rapport de génération des tests

**Date:** 2026-02-13T13:54:32.743813
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order Success

- **Description:** Verify that an order is successfully created when linked to an existing user's email.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Laptop', 'quantity': 1}`
- **Expected output:** JSON containing order_id, user_email 'john.doe@example.com', product_name 'Laptop', and quantity 1

### Test 2: Create Order Failure - User Not Found

- **Description:** Verify that a ValueError is raised when trying to create an order for a user email that does not exist.
- **Inputs:** `{'user_email': 'missing@example.com', 'product_name': 'Mouse', 'quantity': 2}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total Calculation

- **Description:** Verify that the total price is correctly calculated as unit_price multiplied by quantity.
- **Inputs:** `{'unit_price': 25.5, 'quantity': 4}`
- **Expected output:** 102.0

---

## Module: REQ-USER-001

### Test 1: Create User Successfully

- **Description:** Verify that a new user can be created when the email does not exist in the system.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON object with unique id, name 'John Doe', and email 'john.doe@example.com'

### Test 2: Create User Failure - Duplicate Email

- **Description:** Verify that a ValueError is raised when attempting to create a user with an email that already exists.
- **Inputs:** `{'name': 'Jane Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email Success

- **Description:** Verify that the system returns the correct user data for an existing email address.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** User data object containing name and email fields.

### Test 2: Get User By Email Failure

- **Description:** Verify that a ValueError is raised when searching for an email address that is not in the system.
- **Inputs:** `{'email': 'not.found@example.com'}`
- **Expected output:** ValueError

---
