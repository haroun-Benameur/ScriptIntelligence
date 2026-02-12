# Rapport de génération des tests

**Date:** 2026-02-12T14:56:49.144448
**Total tests:** 9
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order is created successfully for a valid user with a quantity greater than 1.
- **Inputs:** `{'user_email': 'jane.doe@example.com', 'product_name': 'Widget A', 'quantity': 2}`
- **Expected output:** JSON containing order_id, user_email 'jane.doe@example.com', product_name 'Widget A', quantity 2

### Test 2: Create Order - User Not Found

- **Description:** Verify that a ValueError is raised when trying to create an order for a non-existent user email.
- **Inputs:** `{'user_email': 'nonexistent@example.com', 'product_name': 'Widget A', 'quantity': 5}`
- **Expected output:** ValueError

### Test 3: Create Order - Invalid Quantity

- **Description:** Verify the system behavior when quantity is 1 or less (requirement states quantity > 1).
- **Inputs:** `{'user_email': 'jane.doe@example.com', 'product_name': 'Widget A', 'quantity': 1}`
- **Expected output:** ValueError or Validation Error

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Success

- **Description:** Verify the calculation logic (unit_price * quantity) for valid inputs where quantity > 10.
- **Inputs:** `{'unit_price': 15.5, 'quantity': 12}`
- **Expected output:** 186.0

### Test 2: Calculate Order Total - Low Quantity Constraint

- **Description:** Verify behavior when quantity is 10 or less (requirement states quantity > 10).
- **Inputs:** `{'unit_price': 10.0, 'quantity': 10}`
- **Expected output:** Error or failure to process calculation as quantity must be > 10

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a user is successfully created when a unique email is provided.
- **Inputs:** `{'name': 'Jane Doe', 'email': 'jane.doe@example.com'}`
- **Expected output:** JSON object with id, name 'Jane Doe', and email 'jane.doe@example.com'

### Test 2: Create User - Duplicate Email

- **Description:** Verify that the system raises a ValueError when attempting to create a user with an email that already exists.
- **Inputs:** `{'name': 'Jane Duplicate', 'email': 'jane.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that user data is returned when searching for an existing email address.
- **Inputs:** `{'email': 'jane.doe@example.com'}`
- **Expected output:** User data object containing user details

### Test 2: Get User By Email - Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist in the system.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
