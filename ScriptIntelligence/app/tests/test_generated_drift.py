"""Tests auto-générés - Ne pas modifier manuellement."""

import pytest
from app import user_service, order_service


def _reset_db():
    user_service.reset_for_testing()
    order_service.reset_for_testing()


def test_0_Create_User___Success():
    _reset_db()

    result = user_service.create_user("Alice Smith", "alice@example.com")
    assert result is not None
    assert hasattr(result, 'email') or hasattr(result, 'name')

def test_1_Create_User___Duplicate_Email_Failure():
    _reset_db()
    user_service.create_user('Existing User', 'alice@example.com')  # setup

    with pytest.raises(ValueError):
        user_service.create_user("Alice Duplicate", "alice@example.com")

def test_2_Get_User_By_Email___Success():
    _reset_db()
    user_service.create_user('Test User', 'alice@example.com')  # setup

    result = user_service.get_user_by_email("alice@example.com")
    assert result is not None
    assert hasattr(result, 'email') or hasattr(result, 'name')

def test_3_Get_User_By_Email___Not_Found():
    _reset_db()

    with pytest.raises(ValueError):
        user_service.get_user_by_email("nonexistent@example.com")

def test_4_Create_Order___Success():
    _reset_db()
    user_service.create_user('Test User', 'alice@example.com')  # setup

    result = order_service.create_order("alice@example.com", "Widget A", 5)
    assert result is not None
    assert hasattr(result, 'order_id') and hasattr(result, 'quantity')

def test_5_Create_Order___User_Does_Not_Exist():
    _reset_db()

    with pytest.raises(ValueError):
        order_service.create_order("unknown@example.com", "Widget A", 1)

def test_6_Create_Order___Invalid_Quantity():
    _reset_db()

    with pytest.raises(ValueError):
        order_service.create_order("alice@example.com", "Widget A", 0)

def test_7_Calculate_Order_Total___Standard_Calculation():
    _reset_db()

    result = order_service.calculate_order_total(20.0, 15)
    assert result == 300.0
