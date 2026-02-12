# Rapport de génération des tests

**Date:** 2026-02-12T14:23:10.683994
**Total tests:** 8
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Success

- **Description:** Verify that an order is created successfully when linked to an existing user email and quantity is greater than 1.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Wireless Mouse', 'quantity': 2}`
- **Expected output:** JSON containing order_id, user_email: 'john.doe@example.com', product_name: 'Wireless Mouse', quantity: 2

### Test 2: Create Order - User Not Found

- **Description:** Verify that a ValueError is raised when creating an order for a user email that does not exist.
- **Inputs:** `{'user_email': 'unknown@example.com', 'product_name': 'Keyboard', 'quantity': 5}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Valid Inputs

- **Description:** Verify that the total price is correctly calculated as unit_price * quantity for inputs satisfying constraints (price > 0, quantity > 10).
- **Inputs:** `{'unit_price': 15.5, 'quantity': 12}`
- **Expected output:** 186.0

### Test 2: Calculate Order Total - Boundary Condition

- **Description:** Verify calculation when quantity is at the minimum threshold defined in requirement (assuming quantity must be > 10).
- **Inputs:** `{'unit_price': 10.0, 'quantity': 11}`
- **Expected output:** 110.0

---

## Module: REQ-USER-001

### Test 1: Create User - Success

- **Description:** Verify that a user is successfully created when a unique email and name are provided.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing id, name: 'John Doe', email: 'john.doe@example.com'

### Test 2: Create User - Duplicate Email

- **Description:** Verify that the system raises a ValueError when attempting to create a user with an email that already exists.
- **Inputs:** `{'name': 'Jane Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Success

- **Description:** Verify that the system returns user data when a valid registered email is provided.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing user data (id, name, email)

### Test 2: Get User By Email - Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist in the system.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
