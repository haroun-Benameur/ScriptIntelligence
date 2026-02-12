# Rapport de génération des tests

**Date:** 2026-02-12T15:28:22.432123
**Total tests:** 10
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Valid Input Success

- **Description:** Verify that an order is successfully created when the user exists and the quantity is greater than 1.
- **Inputs:** `{'user_email': 'valid.user@example.com', 'product_name': 'Mechanical Keyboard', 'quantity': 2}`
- **Expected output:** JSON object with order_id, user_email: 'valid.user@example.com', product_name: 'Mechanical Keyboard', quantity: 2

### Test 2: Create Order - Non-existent User Error

- **Description:** Verify that the system raises a ValueError when attempting to create an order for an email not found in the user management system.
- **Inputs:** `{'user_email': 'nonexistent@example.com', 'product_name': 'Webcam', 'quantity': 5}`
- **Expected output:** ValueError

### Test 3: Create Order - Quantity Boundary Test (Lower)

- **Description:** Verify that an order cannot be created with a quantity of 1, as the requirement specifies quantity must be greater than 1.
- **Inputs:** `{'user_email': 'valid.user@example.com', 'product_name': 'USB Cable', 'quantity': 1}`
- **Expected output:** ValueError

### Test 4: Create Order - Missing User Email

- **Description:** Verify that missing the required user_email input results in a failure.
- **Inputs:** `{'product_name': 'Laptop', 'quantity': 2}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Valid

- **Description:** Ensure the total price is correctly calculated for quantities greater than 10.
- **Inputs:** `{'unit_price': 50.0, 'quantity': 12}`
- **Expected output:** 600.0

### Test 2: Calculate Order Total - Boundary Condition

- **Description:** Verify calculation works at the minimum required quantity threshold (e.g., 11).
- **Inputs:** `{'unit_price': 10.0, 'quantity': 11}`
- **Expected output:** 110.0

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Ensure a user can be successfully created when the email does not exist.
- **Inputs:** `{'name': 'Alice Smith', 'email': 'alice@example.com'}`
- **Expected output:** JSON containing a unique id, name 'Alice Smith', and email 'alice@example.com'.

### Test 2: Create User - Duplicate Email

- **Description:** Ensure the system raises a ValueError when attempting to create a user with an existing email.
- **Inputs:** `{'name': 'Alice Jones', 'email': 'alice@example.com'}`
- **Expected output:** Raise ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Ensure user data is returned when a valid, existing email is provided.
- **Inputs:** `{'email': 'alice@example.com'}`
- **Expected output:** User data matching the email 'alice@example.com'.

### Test 2: Get User By Email - Not Found

- **Description:** Ensure the system raises a ValueError when the email does not exist in the database.
- **Inputs:** `{'email': 'unknown@example.com'}`
- **Expected output:** Raise ValueError

---
