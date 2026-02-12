# Rapport de génération des tests

**Date:** 2026-02-12T10:35:45.336572
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order is successfully created for an existing user.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Widget A', 'quantity': 5}`
- **Expected output:** JSON containing order_id, user_email: 'john.doe@example.com', product_name: 'Widget A', quantity: 5

### Test 2: Create Order - Invalid User

- **Description:** Verify that a ValueError is raised when creating an order for a user email that does not exist.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Widget A', 'quantity': 1}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Success

- **Description:** Verify the total price calculation (unit_price * quantity) for valid inputs.
- **Inputs:** `{'unit_price': 15.5, 'quantity': 12}`
- **Expected output:** 186.0

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a new user is successfully created when a unique email is provided.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON object containing id, name: 'John Doe', email: 'john.doe@example.com'

### Test 2: Create User - Duplicate Email

- **Description:** Verify that a ValueError is raised when attempting to create a user with an email that already exists.
- **Inputs:** `{'name': 'Jane Smith', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that the system returns the correct user data when a valid, existing email is provided.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** User data object matching the provided email

### Test 2: Get User By Email - Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist in the system.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
