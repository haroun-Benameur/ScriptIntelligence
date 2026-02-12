# Rapport de génération des tests

**Date:** 2026-02-12T10:34:25.617139
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order for Valid User

- **Description:** Verify that an order is successfully created when linked to a valid user email.
- **Inputs:** `{'user_email': 'alice@example.com', 'product_name': 'Mechanical Keyboard', 'quantity': 1}`
- **Expected output:** JSON object with order_id, user_email: 'alice@example.com', product_name: 'Mechanical Keyboard', quantity: 1

### Test 2: Create Order for Invalid User

- **Description:** Verify that a ValueError is raised when creating an order for an email that does not exist in the user management system.
- **Inputs:** `{'user_email': 'nonexistent@example.com', 'product_name': 'Mechanical Keyboard', 'quantity': 1}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total Correctness

- **Description:** Verify that the total is calculated correctly as unit_price multiplied by quantity.
- **Inputs:** `{'unit_price': 25.5, 'quantity': 12}`
- **Expected output:** 306.0

---

## Module: REQ-USER-001

### Test 1: Successful User Creation

- **Description:** Verify that a new user is created when the email is unique.
- **Inputs:** `{'name': 'Alice Smith', 'email': 'alice@example.com'}`
- **Expected output:** JSON object with id, name: 'Alice Smith', email: 'alice@example.com'

### Test 2: Duplicate Email Creation Failure

- **Description:** Verify that a ValueError is raised when attempting to create a user with an email that already exists.
- **Inputs:** `{'name': 'Alice Duplicate', 'email': 'alice@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get Existing User by Email

- **Description:** Verify that user data is returned correctly for an existing email address.
- **Inputs:** `{'email': 'alice@example.com'}`
- **Expected output:** User data object corresponding to alice@example.com

### Test 2: Get Non-existent User

- **Description:** Verify that a ValueError is raised when requesting a user with an email that is not in the system.
- **Inputs:** `{'email': 'unknown@example.com'}`
- **Expected output:** ValueError

---
