"""Tests auto-générés - Ne pas modifier manuellement."""

import pytest
from app import user_service, order_service


def _reset_db():
    user_service.reset_for_testing()
    order_service.reset_for_testing()


def test_0_Successful_Order_Creation():
    _reset_db()
    user_service.create_user('Test User', 'valid.user@example.com')  # setup

    result = order_service.create_order("valid.user@example.com", "Mechanical Keyboard", 2)
    assert result is not None
    assert hasattr(result, 'order_id') and hasattr(result, 'quantity')

def test_1_Order_Creation_Failure___User_Does_Not_Exist():
    _reset_db()

    with pytest.raises(ValueError):
        order_service.create_order("nonexistent@example.com", "Mechanical Keyboard", 2)

def test_2_Order_Creation_Failure___Invalid_Quantity__Boundary_():
    _reset_db()

    with pytest.raises(ValueError):
        order_service.create_order("valid.user@example.com", "Mechanical Keyboard", 1)

def test_3_Order_Creation_Failure___Negative_Quantity():
    _reset_db()

    with pytest.raises(ValueError):
        order_service.create_order("valid.user@example.com", "Mechanical Keyboard", -5)
