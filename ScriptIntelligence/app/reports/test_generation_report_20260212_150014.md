# Rapport de génération des tests

**Date:** 2026-02-12T15:00:14.490055
**Total tests:** 7
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create order for existing user success

- **Description:** Verify that an order is created successfully when the user exists and quantity is greater than 1.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Laptop', 'quantity': 2}`
- **Expected output:** JSON object containing order_id, user_email='john.doe@example.com', product_name='Laptop', quantity=2

### Test 2: Create order for non-existent user failure

- **Description:** Verify that a ValueError is raised when creating an order for an email not registered in the system.
- **Inputs:** `{'user_email': 'ghost@example.com', 'product_name': 'Laptop', 'quantity': 2}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate order total successfully

- **Description:** Verify that the total price is calculated as unit_price multiplied by quantity.
- **Inputs:** `{'unit_price': 50.0, 'quantity': 11}`
- **Expected output:** 550.0

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

---
