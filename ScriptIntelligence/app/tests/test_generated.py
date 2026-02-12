"""Tests auto-générés - Ne pas modifier manuellement."""

import pytest
from app import user_service, order_service


def _reset_db():
    user_service.reset_for_testing()
    order_service.reset_for_testing()


def test_0_Create_User___Success():
    _reset_db()

    result = user_service.create_user("John Doe", "john.doe@example.com")
    assert result is not None
    assert hasattr(result, 'email') or hasattr(result, 'name')

def test_1_Create_User___Duplicate_Email_Error():
    _reset_db()
    user_service.create_user('Existing User', 'john.doe@example.com')  # setup

    with pytest.raises(ValueError):
        user_service.create_user("Jane Doe", "john.doe@example.com")

def test_2_Get_User_By_Email___Success():
    _reset_db()
    user_service.create_user('Test User', 'john.doe@example.com')  # setup

    result = user_service.get_user_by_email("john.doe@example.com")
    assert result is not None
    assert hasattr(result, 'email') or hasattr(result, 'name')

def test_3_Get_User_By_Email___Not_Found():
    _reset_db()

    with pytest.raises(ValueError):
        user_service.get_user_by_email("missing@example.com")

def test_4_Create_Order___Valid_User():
    _reset_db()
    user_service.create_user('Test User', 'john.doe@example.com')  # setup

    result = order_service.create_order("john.doe@example.com", "Smartphone", 1)
    assert result is not None
    assert hasattr(result, 'order_id') and hasattr(result, 'quantity')

def test_5_Create_Order___Invalid_User():
    _reset_db()

    with pytest.raises(ValueError):
        order_service.create_order("nonexistent@example.com", "Smartphone", 1)

def test_6_Calculate_Order_Total___Standard_Calculation():
    _reset_db()

    result = order_service.calculate_order_total(10.5, 20)
    assert result == 210.0
