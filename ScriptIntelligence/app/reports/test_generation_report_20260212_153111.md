# Rapport de génération des tests

**Date:** 2026-02-12T15:31:11.750397
**Total tests:** 13
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order is created successfully when linked to an existing user email.
- **Inputs:** `{'user_email': 'alice@example.com', 'product_name': 'Widget A', 'quantity': 5}`
- **Expected output:** JSON containing order_id, user_email: 'alice@example.com', product_name: 'Widget A', quantity: 5

### Test 2: Create Order - User Does Not Exist

- **Description:** Verify that order creation fails with a ValueError if the provided user email is not found in the system.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Widget A', 'quantity': 1}`
- **Expected output:** ValueError

### Test 3: Create Order - Invalid Quantity

- **Description:** Verify that order creation fails if the quantity is 0 or less, as per the requirement 'quantity (int > 0)'.
- **Inputs:** `{'user_email': 'alice@example.com', 'product_name': 'Widget A', 'quantity': 0}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total Correctness

- **Description:** Verify that the total price is calculated correctly by multiplying unit price and quantity.
- **Inputs:** `{'unit_price': 15.5, 'quantity': 20}`
- **Expected output:** 310.0

### Test 2: Calculate Order Total - Standard Calculation

- **Description:** Verify that the total price is calculated correctly based on unit_price * quantity.
- **Inputs:** `{'unit_price': 20.0, 'quantity': 15}`
- **Expected output:** 300.0

---

## Module: REQ-USER-001

### Test 1: Create New User Success

- **Description:** Verify that a user is successfully created when the email is unique.
- **Inputs:** `{'name': 'Alice Smith', 'email': 'alice.smith@example.com'}`
- **Expected output:** JSON containing generated id, name: 'Alice Smith', email: 'alice.smith@example.com'

### Test 2: Create User Duplicate Email Failure

- **Description:** Verify that a ValueError is raised when attempting to create a user with an existing email.
- **Inputs:** `{'name': 'Alice Duplicate', 'email': 'alice.smith@example.com'}`
- **Expected output:** ValueError

### Test 3: Create User - Success

- **Description:** Verify that a user is successfully created when the email is unique.
- **Inputs:** `{'name': 'Alice Smith', 'email': 'alice@example.com'}`
- **Expected output:** JSON containing generated id, name: 'Alice Smith', email: 'alice@example.com'

### Test 4: Create User - Duplicate Email Failure

- **Description:** Verify that attempting to create a user with an already registered email raises a ValueError.
- **Inputs:** `{'name': 'Alice Duplicate', 'email': 'alice@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get Existing User By Email

- **Description:** Verify that the system returns correct user data when a valid email is provided.
- **Inputs:** `{'email': 'alice.smith@example.com'}`
- **Expected output:** JSON object with user data (id, name, email)

### Test 2: Get User By Email Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

### Test 3: Get User By Email - Success

- **Description:** Verify that user data is returned when a valid registered email is provided.
- **Inputs:** `{'email': 'alice@example.com'}`
- **Expected output:** JSON object containing user details for alice@example.com

### Test 4: Get User By Email - Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
