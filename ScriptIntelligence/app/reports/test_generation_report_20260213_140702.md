# Rapport de génération des tests

**Date:** 2026-02-13T14:07:02.158717
**Total tests:** 10
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Successful Order Creation

- **Description:** Verify that an order is created successfully when the user exists and the quantity is greater than 1.
- **Inputs:** `{'user_email': 'valid.user@example.com', 'product_name': 'Mechanical Keyboard', 'quantity': 2}`
- **Expected output:** JSON containing order_id, user_email 'valid.user@example.com', product_name 'Mechanical Keyboard', and quantity 2.

### Test 2: Order Creation Failure - User Does Not Exist

- **Description:** Verify that the system raises a ValueError when attempting to create an order for a non-existent user email.
- **Inputs:** `{'user_email': 'nonexistent@example.com', 'product_name': 'Mechanical Keyboard', 'quantity': 2}`
- **Expected output:** ValueError

### Test 3: Order Creation Failure - Invalid Quantity (Boundary)

- **Description:** Verify that the system raises a ValueError or validation error when the quantity is 1, as the requirement specifies quantity > 1.
- **Inputs:** `{'user_email': 'valid.user@example.com', 'product_name': 'Mechanical Keyboard', 'quantity': 1}`
- **Expected output:** ValueError

### Test 4: Order Creation Failure - Negative Quantity

- **Description:** Verify that the system raises a ValueError when the quantity is less than 1.
- **Inputs:** `{'user_email': 'valid.user@example.com', 'product_name': 'Mechanical Keyboard', 'quantity': -5}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total Calculation

- **Description:** Verify that the system correctly calculates the total price based on unit_price and quantity.
- **Inputs:** `{'unit_price': 49.99, 'quantity': 3}`
- **Expected output:** 149.97

### Test 2: Calculate Order Total Boundary

- **Description:** Verify calculation with minimum valid values.
- **Inputs:** `{'unit_price': 0.01, 'quantity': 1}`
- **Expected output:** 0.01

---

## Module: REQ-USER-001

### Test 1: Create New User Success

- **Description:** Verify that a new user is successfully created when a unique email is provided.
- **Inputs:** `{'name': 'Alice Smith', 'email': 'alice.smith@example.com'}`
- **Expected output:** JSON containing a generated id, name: 'Alice Smith', and email: 'alice.smith@example.com'.

### Test 2: Create User Duplicate Email

- **Description:** Verify that a ValueError is raised when attempting to create a user with an email that already exists in the system.
- **Inputs:** `{'name': 'Alice Duplicate', 'email': 'alice.smith@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email Success

- **Description:** Verify that the system returns the correct user data when a valid, existing email is provided.
- **Inputs:** `{'email': 'alice.smith@example.com'}`
- **Expected output:** JSON object containing user details for alice.smith@example.com.

### Test 2: Get User By Email Not Found

- **Description:** Verify that the system raises a ValueError when attempting to retrieve a user using an email that does not exist.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
