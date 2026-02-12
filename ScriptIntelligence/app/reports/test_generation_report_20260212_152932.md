# Rapport de génération des tests

**Date:** 2026-02-12T15:29:32.410819
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order Linked to User Success

- **Description:** Verify that an order is successfully created for an existing user.
- **Inputs:** `{'user_email': 'alice.smith@example.com', 'product_name': 'Gadget X', 'quantity': 5}`
- **Expected output:** JSON containing order_id, user_email: 'alice.smith@example.com', product_name: 'Gadget X', quantity: 5

### Test 2: Create Order User Not Found Failure

- **Description:** Verify that a ValueError is raised when creating an order for a non-existent user.
- **Inputs:** `{'user_email': 'ghost@example.com', 'product_name': 'Gadget X', 'quantity': 5}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total Correctness

- **Description:** Verify that the total price is calculated correctly by multiplying unit price and quantity.
- **Inputs:** `{'unit_price': 15.5, 'quantity': 20}`
- **Expected output:** 310.0

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

---
