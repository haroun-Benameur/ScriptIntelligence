# app/order_service.py

from app.models import Order
from app.user_service import get_user_by_email

orders_db = []
order_id_counter = 1


def create_order(user_email: str, product_name: str, quantity: int) -> Order:
    global order_id_counter

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")

    # Verify user exists
    get_user_by_email(user_email)

    new_order = Order(
        order_id=order_id_counter,
        user_email=user_email,
        product_name=product_name,
        quantity=quantity
    )

    orders_db.append(new_order)
    order_id_counter += 1

    return new_order


def calculate_order_total(unit_price: float, quantity: int) -> float:
    if unit_price <= 0:
        raise ValueError("Unit price must be positive")

    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    return unit_price * quantity


def reset_for_testing() -> None:
    """Reset DB for pytest isolation. Use only in tests."""
    global order_id_counter, orders_db
    orders_db = []
    order_id_counter = 1
