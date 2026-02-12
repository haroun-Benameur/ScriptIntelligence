# Rapport de génération des tests

**Date:** 2026-02-12T11:05:00.982915
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order Linked to User

- **Description:** Verify that an order is successfully created and linked when the user email exists.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Wireless Mouse', 'quantity': -1}`
- **Expected output:** JSON containing order_id, user_email: "john.doe@example.com", product_name: "Wireless Mouse", and quantity: -1

### Test 2: Create Order User Not Found

- **Description:** Verify that a ValueError is raised when trying to create an order for a non-existent user email.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Keyboard', 'quantity': -5}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total Valid Range

- **Description:** Verify the calculation of the total price (unit_price * quantity) for valid inputs.
- **Inputs:** `{'unit_price': 15.5, 'quantity': 20}`
- **Expected output:** 310.0

---

## Module: REQ-USER-001

### Test 1: Create New User Success

- **Description:** Verify that a new user is created successfully when the email is unique.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing a generated id, name: "John Doe", and email: "john.doe@example.com"

### Test 2: Create User Duplicate Email

- **Description:** Verify that a ValueError is raised when attempting to create a user with an email that already exists in the system.
- **Inputs:** `{'name': 'John Smith', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email Success

- **Description:** Verify that user data is returned when a valid, existing email is provided.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** JSON object with user details (id, name, email) for the specified email.

### Test 2: Get User By Email Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
