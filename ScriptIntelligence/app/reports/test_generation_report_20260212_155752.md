# Rapport de génération des tests

**Date:** 2026-02-12T15:57:52.260661
**Total tests:** 8
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order can be created for an existing user.
- **Inputs:** `{'user_email': 'jane.doe@example.com', 'product_name': 'Widget A', 'quantity': 5}`
- **Expected output:** JSON containing order_id, user_email: 'jane.doe@example.com', product_name: 'Widget A', quantity: 5

### Test 2: Create Order - User Missing

- **Description:** Verify that a ValueError is raised if the user_email provided does not exist.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Widget A', 'quantity': 1}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Standard

- **Description:** Verify calculation of total price (unit_price * quantity) where quantity > 10.
- **Inputs:** `{'unit_price': 10.0, 'quantity': 15}`
- **Expected output:** 150.0

### Test 2: Calculate Order Total - Boundary Floating Point

- **Description:** Verify calculation with float unit prices.
- **Inputs:** `{'unit_price': 9.99, 'quantity': 20}`
- **Expected output:** 199.8

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a new user is created successfully when a unique email is provided.
- **Inputs:** `{'name': 'Jane Doe', 'email': 'jane.doe@example.com'}`
- **Expected output:** JSON containing generated id, name: 'Jane Doe', email: 'jane.doe@example.com'

### Test 2: Create User - Duplicate Email

- **Description:** Verify that a ValueError is raised when attempting to create a user with an email that already exists.
- **Inputs:** `{'name': 'Jane Smith', 'email': 'jane.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that user data is returned when a valid existing email is provided.
- **Inputs:** `{'email': 'jane.doe@example.com'}`
- **Expected output:** JSON containing user data (id, name, email)

### Test 2: Get User By Email - Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist in the system.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
