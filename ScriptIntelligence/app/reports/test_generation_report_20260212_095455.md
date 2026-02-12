# Rapport de génération des tests

**Date:** 2026-02-12T09:54:55.317669
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order is created successfully when linked to an existing user email.
- **Inputs:** `{'user_email': 'jane.doe@example.com', 'product_name': 'Wireless Mouse', 'quantity': 2}`
- **Expected output:** A JSON object containing order_id, user_email='jane.doe@example.com', product_name='Wireless Mouse', and quantity=2.

### Test 2: Create Order - Missing User

- **Description:** Verify that a ValueError is raised when attempting to create an order for an email that does not exist.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Wireless Mouse', 'quantity': 1}`
- **Expected output:** Raise ValueError.

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Logic Check

- **Description:** Verify that the system returns the correct product of unit_price and quantity.
- **Inputs:** `{'unit_price': 25.5, 'quantity': 11}`
- **Expected output:** 280.5

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a new user can be created with a unique email address.
- **Inputs:** `{'name': 'Jane Doe', 'email': 'jane.doe@example.com'}`
- **Expected output:** A JSON object containing the user id, 'Jane Doe', and 'jane.doe@example.com'.

### Test 2: Create User - Duplicate Email

- **Description:** Verify that a ValueError is raised if the email already exists in the system.
- **Inputs:** `{'name': 'Duplicate User', 'email': 'jane.doe@example.com'}`
- **Expected output:** Raise ValueError.

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that the system returns the correct user data for an existing email.
- **Inputs:** `{'email': 'jane.doe@example.com'}`
- **Expected output:** A JSON object containing the user data associated with 'jane.doe@example.com'.

### Test 2: Get User By Email - Not Found

- **Description:** Verify that a ValueError is raised if the email does not exist in the system.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** Raise ValueError.

---
