# Rapport de génération des tests

**Date:** 2026-02-12T15:03:30.228031
**Total tests:** 14
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order is successfully created and linked to an existing user.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Mechanical Keyboard', 'quantity': 2}`
- **Expected output:** JSON object with order_id, user_email 'john.doe@example.com', product_name 'Mechanical Keyboard', and quantity 2.

### Test 2: Create Order - Missing User

- **Description:** Verify that creating an order for an email not registered in the system raises a ValueError.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Mouse', 'quantity': 1}`
- **Expected output:** ValueError

### Test 3: Create Order - Invalid Quantity

- **Description:** Verify that an order cannot be created with a quantity of 0 or less.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Webcam', 'quantity': 0}`
- **Expected output:** ValueError or Error indicating quantity must be > 0.

---

## Module: REQ-ORDER-002

### Test 1: Calculate order total successfully

- **Description:** Verify that the total price is calculated as unit_price multiplied by quantity.
- **Inputs:** `{'unit_price': 50.0, 'quantity': 11}`
- **Expected output:** 550.0

### Test 2: Calculate Order Total - Success

- **Description:** Verify the calculation of total price for valid unit price and quantity > 10.
- **Inputs:** `{'unit_price': 25.5, 'quantity': 12}`
- **Expected output:** 306.0

### Test 3: Calculate Order Total - Minimum Quantity Constraint

- **Description:** Verify behavior when quantity is at or below the specified threshold of 10.
- **Inputs:** `{'unit_price': 10.0, 'quantity': 5}`
- **Expected output:** Error or failure to process calculation based on input constraint (quantity > 10).

---

## Module: REQ-USER-001

### Test 1: Create user success

- **Description:** Verify that a new user is created successfully when the email is unique.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON object with id, name='John Doe', email='john.doe@example.com'

### Test 2: Create user duplicate email failure

- **Description:** Verify that a ValueError is raised when trying to create a user with an email that already exists.
- **Inputs:** `{'name': 'Jane Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

### Test 3: Create User - Success

- **Description:** Verify that a new user is created successfully when the email does not exist in the system.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** User object created with a unique ID, name 'John Doe', and email 'john.doe@example.com'.

### Test 4: Create User - Duplicate Email

- **Description:** Verify that the system raises a ValueError when attempting to create a user with an email that already exists.
- **Inputs:** `{'name': 'John Duplicate', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get existing user by email

- **Description:** Verify that the system returns user data for an existing email address.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** User data object matching the provided email

### Test 2: Get non-existent user by email failure

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist in the system.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

### Test 3: Get User By Email - Success

- **Description:** Verify that user data is returned correctly when searching with a valid existing email.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** User data object containing user details for john.doe@example.com.

### Test 4: Get User By Email - Not Found

- **Description:** Verify that searching for a non-existent email raises a ValueError.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
