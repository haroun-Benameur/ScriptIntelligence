# Rapport de génération des tests

**Date:** 2026-02-12T11:38:12.051697
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Valid Order

- **Description:** Verify that an order is successfully created when the user exists and quantity is greater than 1.
- **Inputs:** `{'user_email': 'alice@example.com', 'product_name': 'Widget A', 'quantity': 2}`
- **Expected output:** JSON containing order_id, user_email 'alice@example.com', product_name 'Widget A', and quantity 2.

### Test 2: Order Creation User Not Found

- **Description:** Verify that an order cannot be created for a user email that does not exist in the system.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Widget A', 'quantity': 5}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total Correctness

- **Description:** Verify that the system correctly calculates total price (unit_price * quantity) for valid inputs.
- **Inputs:** `{'unit_price': 15.5, 'quantity': 12}`
- **Expected output:** 186.0

---

## Module: REQ-USER-001

### Test 1: Successful User Creation

- **Description:** Verify that a new user is created when a unique email and valid name are provided.
- **Inputs:** `{'name': 'Alice Smith', 'email': 'alice@example.com'}`
- **Expected output:** JSON object with id, name 'Alice Smith', and email 'alice@example.com'.

### Test 2: Duplicate User Email Prevention

- **Description:** Verify that the system raises a ValueError when attempting to create a user with an email that already exists.
- **Inputs:** `{'name': 'Alice Duplicate', 'email': 'alice@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User by Valid Email

- **Description:** Verify that user data is returned when searching with an existing email.
- **Inputs:** `{'email': 'alice@example.com'}`
- **Expected output:** User data object containing name and email.

### Test 2: Get Non-existent User

- **Description:** Verify that searching for a user email that does not exist raises a ValueError.
- **Inputs:** `{'email': 'missing@example.com'}`
- **Expected output:** ValueError

---
