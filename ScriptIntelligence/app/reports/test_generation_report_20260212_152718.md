# Rapport de génération des tests

**Date:** 2026-02-12T15:27:18.535659
**Total tests:** 10
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success Scenario

- **Description:** Verify that a valid order is created when the user email exists in the system.
- **Inputs:** `{'user_email': 'existing_user@example.com', 'product_name': 'Laptop', 'quantity': 2}`
- **Expected output:** JSON containing order_id, user_email: 'existing_user@example.com', product_name: 'Laptop', quantity: 2

### Test 2: Create Order - Non-existent User

- **Description:** Verify that a ValueError is raised when trying to create an order for a user email that does not exist.
- **Inputs:** `{'user_email': 'non_existent@example.com', 'product_name': 'Laptop', 'quantity': 1}`
- **Expected output:** ValueError

### Test 3: Create Order - Boundary Quantity (Zero)

- **Description:** Verify that the system enforces the quantity constraint (int > 0) and fails if quantity is 0.
- **Inputs:** `{'user_email': 'existing_user@example.com', 'product_name': 'Laptop', 'quantity': 0}`
- **Expected output:** ValueError or validation error indicating quantity must be greater than zero

### Test 4: Create Order - Negative Quantity

- **Description:** Verify that the system enforces the quantity constraint (int > 0) and fails if quantity is negative.
- **Inputs:** `{'user_email': 'existing_user@example.com', 'product_name': 'Laptop', 'quantity': -5}`
- **Expected output:** ValueError or validation error indicating quantity must be greater than zero

### Test 5: Create Order - Integration with REQ-USER-001

- **Description:** Verify order creation after a new user is successfully created via the User Management system.
- **Inputs:** `{'user_email': 'newly_created@example.com', 'product_name': 'Desk', 'quantity': 1}`
- **Expected output:** JSON containing order_id and order details linked to newly_created@example.com

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Success

- **Description:** Verify that the total price is calculated as unit_price multiplied by quantity.
- **Inputs:** `{'unit_price': 15.5, 'quantity': 12}`
- **Expected output:** 186.0

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a new user is successfully created when a unique email is provided.
- **Inputs:** `{'name': 'Alice Smith', 'email': 'alice@example.com'}`
- **Expected output:** JSON object with id, name='Alice Smith', email='alice@example.com'

### Test 2: Create User - Duplicate Email

- **Description:** Verify that creating a user with an already existing email raises a ValueError.
- **Inputs:** `{'name': 'Alice Duplicate', 'email': 'alice@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that user data is returned when searching for an existing email.
- **Inputs:** `{'email': 'alice@example.com'}`
- **Expected output:** User data object matching alice@example.com

### Test 2: Get User By Email - Not Found

- **Description:** Verify that searching for a non-existent email raises a ValueError.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
