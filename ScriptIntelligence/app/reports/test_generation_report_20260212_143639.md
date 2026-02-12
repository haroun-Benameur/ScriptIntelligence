# Rapport de génération des tests

**Date:** 2026-02-12T14:36:39.277401
**Total tests:** 8
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order is created successfully for an existing user.
- **Inputs:** `{'user_email': 'jane.doe@example.com', 'product_name': 'Widget', 'quantity': 5}`
- **Expected output:** JSON containing order_id, user_email: 'jane.doe@example.com', product_name: 'Widget', quantity: 5

### Test 2: Create Order - Non-existent User

- **Description:** Verify that a ValueError is raised when creating an order for a user email that does not exist.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Widget', 'quantity': 5}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Success

- **Description:** Verify that the total price is calculated correctly (unit_price * quantity) for valid inputs.
- **Inputs:** `{'unit_price': 15.5, 'quantity': 20}`
- **Expected output:** 310.0

### Test 2: Calculate Order Total - Minimum Quantity Validation

- **Description:** Verify system behavior when quantity is at or below the threshold defined in the spec (>10).
- **Inputs:** `{'unit_price': 10.0, 'quantity': 5}`
- **Expected output:** Specific behavior depends on implementation of constraint validation, typically an Exception or Error.

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a new user is created successfully when providing a unique email.
- **Inputs:** `{'name': 'Jane Doe', 'email': 'jane.doe@example.com'}`
- **Expected output:** JSON containing generated id, name: 'Jane Doe', email: 'jane.doe@example.com'

### Test 2: Create User - Duplicate Email

- **Description:** Verify that the system raises a ValueError when attempting to create a user with an existing email.
- **Inputs:** `{'name': 'Duplicate User', 'email': 'jane.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that user data is returned when searching for an existing email.
- **Inputs:** `{'email': 'jane.doe@example.com'}`
- **Expected output:** User object with name 'Jane Doe' and email 'jane.doe@example.com'

### Test 2: Get User By Email - Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
