# Rapport de génération des tests

**Date:** 2026-02-12T15:06:49.317611
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order For Existing User

- **Description:** Verify that an order is successfully created when linked to an existing user's email.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Widget A', 'quantity': 5}`
- **Expected output:** JSON containing order_id, user_email 'john.doe@example.com', product_name 'Widget A', and quantity 5.

### Test 2: Create Order For Non-Existent User

- **Description:** Verify that a ValueError is raised when creating an order for an email not registered in the system.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Widget A', 'quantity': 5}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total Price

- **Description:** Verify that the system returns the product of unit_price and quantity.
- **Inputs:** `{'unit_price': 15.5, 'quantity': 20}`
- **Expected output:** 310.0

---

## Module: REQ-USER-001

### Test 1: Create New User Successfully

- **Description:** Verify that a user is created when the email does not exist in the system.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing a unique id, name 'John Doe', and email 'john.doe@example.com'.

### Test 2: Create User Duplicate Email

- **Description:** Verify that a ValueError is raised when attempting to create a user with an email that already exists.
- **Inputs:** `{'name': 'Jane Smith', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Existing Email

- **Description:** Verify that user data is correctly retrieved when searching by a valid existing email.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** User object containing data for john.doe@example.com.

### Test 2: Get User By Non-Existent Email

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist.
- **Inputs:** `{'email': 'missing@example.com'}`
- **Expected output:** ValueError

---
