# Rapport de génération des tests

**Date:** 2026-02-12T11:14:52.891248
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Valid User

- **Description:** Verify that an order is created successfully when linked to an existing user.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Smartphone', 'quantity': 1}`
- **Expected output:** JSON object with order_id, user_email: 'john.doe@example.com', product_name: 'Smartphone', quantity: 1

### Test 2: Create Order - Invalid User

- **Description:** Verify that creating an order for a user email that does not exist raises a ValueError.
- **Inputs:** `{'user_email': 'nonexistent@example.com', 'product_name': 'Smartphone', 'quantity': 1}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Standard Calculation

- **Description:** Verify that the system correctly calculates total price as unit_price * quantity.
- **Inputs:** `{'unit_price': 10.5, 'quantity': 20}`
- **Expected output:** 210.0

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a user is successfully created when a unique email is provided.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON object with unique id, name: 'John Doe', email: 'john.doe@example.com'

### Test 2: Create User - Duplicate Email Error

- **Description:** Verify that attempting to create a user with an email that already exists raises a ValueError.
- **Inputs:** `{'name': 'Jane Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that the system returns the correct user data for an existing email address.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** User data object matching the email 'john.doe@example.com'

### Test 2: Get User By Email - Not Found

- **Description:** Verify that searching for a non-existent email raises a ValueError.
- **Inputs:** `{'email': 'missing@example.com'}`
- **Expected output:** ValueError

---
