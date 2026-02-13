"""Tests auto-générés - Ne pas modifier manuellement."""

import pytest
from app import user_service, order_service


def _reset_db():
    user_service.reset_for_testing()
    order_service.reset_for_testing()


def test_0_Create_User___Successful():
    _reset_db()

    result = user_service.create_user("John Doe", "john.doe@example.com")
    assert result is not None
    assert hasattr(result, 'email') or hasattr(result, 'name')

def test_1_Create_User___Duplicate_Email():
    _reset_db()
    user_service.create_user('Existing User', 'john.doe@example.com')  # setup

    with pytest.raises(ValueError):
        user_service.create_user("Jane Doe", "john.doe@example.com")

def test_2_Get_User_By_Email___Found():
    _reset_db()
    user_service.create_user('Test User', 'john.doe@example.com')  # setup

    result = user_service.get_user_by_email("john.doe@example.com")
    assert result is not None
    assert hasattr(result, 'email') or hasattr(result, 'name')

def test_3_Get_User_By_Email___Not_Found():
    _reset_db()

    with pytest.raises(ValueError):
        user_service.get_user_by_email("nonexistent@example.com")

def test_4_Create_Order___Successful():
    _reset_db()
    user_service.create_user('Test User', 'john.doe@example.com')  # setup

    result = order_service.create_order("john.doe@example.com", "Widget A", 5)
    assert result is not None
    assert hasattr(result, 'order_id') and hasattr(result, 'quantity')

def test_5_Create_Order___User_Not_Found():
    _reset_db()

    with pytest.raises(ValueError):
        order_service.create_order("ghost@example.com", "Widget A", 5)

def test_6_Create_Order___Invalid_Quantity():
    _reset_db()

    with pytest.raises(ValueError):
        order_service.create_order("john.doe@example.com", "Widget A", 1)

def test_7_Calculate_Order_Total___Normal_Case():
    _reset_db()

    result = order_service.calculate_order_total(15.5, 4)
    assert result == 62.0

def test_8_Calculate_Order_Total___Decimals():
    _reset_db()

    result = order_service.calculate_order_total(10.99, 2)
    assert result == 21.98
