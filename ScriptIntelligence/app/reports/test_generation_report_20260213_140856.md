# Rapport de génération des tests

**Date:** 2026-02-13T14:08:56.186000
**Total tests:** 9
**Modules:** 4

---

## Module: REQ-ORDER-001

### Test 1: Create Order - Successful

- **Description:** Verify that an order is created when the user exists and the quantity is greater than 1.
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Widget A', 'quantity': 5}`
- **Expected output:** JSON containing order_id, user_email: 'john.doe@example.com', product_name: 'Widget A', quantity: 5

### Test 2: Create Order - User Not Found

- **Description:** Verify that a ValueError is raised when creating an order for an email that is not registered.
- **Inputs:** `{'user_email': 'ghost@example.com', 'product_name': 'Widget A', 'quantity': 5}`
- **Expected output:** ValueError

### Test 3: Create Order - Invalid Quantity

- **Description:** Verify that a ValueError is raised if the quantity is not greater than 1 (Boundary test: quantity = 1).
- **Inputs:** `{'user_email': 'john.doe@example.com', 'product_name': 'Widget A', 'quantity': 1}`
- **Expected output:** ValueError

---

## Module: REQ-ORDER-002

### Test 1: Calculate Order Total - Normal Case

- **Description:** Verify the calculation of the total price given a positive unit price and quantity.
- **Inputs:** `{'unit_price': 15.5, 'quantity': 4}`
- **Expected output:** 62.0

### Test 2: Calculate Order Total - Decimals

- **Description:** Verify accuracy of the total price calculation with fractional prices.
- **Inputs:** `{'unit_price': 10.99, 'quantity': 2}`
- **Expected output:** 21.98

---

## Module: REQ-USER-001

### Test 1: Create User - Successful

- **Description:** Verify that a user is successfully created when a unique email is provided.
- **Inputs:** `{'name': 'John Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** JSON containing generated id, name: 'John Doe', email: 'john.doe@example.com'

### Test 2: Create User - Duplicate Email

- **Description:** Verify that a ValueError is raised when attempting to create a user with an email that already exists in the system.
- **Inputs:** `{'name': 'Jane Doe', 'email': 'john.doe@example.com'}`
- **Expected output:** ValueError

---

## Module: REQ-USER-002

### Test 1: Get User By Email - Found

- **Description:** Verify that user data is returned when searching for an existing email address.
- **Inputs:** `{'email': 'john.doe@example.com'}`
- **Expected output:** JSON object with user details matching 'john.doe@example.com'

### Test 2: Get User By Email - Not Found

- **Description:** Verify that a ValueError is raised when searching for an email that does not exist.
- **Inputs:** `{'email': 'nonexistent@example.com'}`
- **Expected output:** ValueError

---
