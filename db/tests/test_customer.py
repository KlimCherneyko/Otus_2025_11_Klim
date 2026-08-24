import uuid

from lib.db import (
    create_customer,
    delete_customer,
    get_customer_by_id,
    update_customer,
)


def _customer_data(**overrides):
    unique = uuid.uuid4().hex[:8]
    data = {
        "firstname": "Test",
        "lastname": "User",
        "email": f"test_{unique}@example.com",
        "telephone": "1234567890",
    }
    data.update(overrides)
    return data


def test_create_customer(connection):
    customer_data = _customer_data()
    customer_id = create_customer(connection, customer_data)

    customer = get_customer_by_id(connection, customer_id)
    assert customer is not None
    assert customer["customer_id"] == customer_id
    assert customer["firstname"] == customer_data["firstname"]
    assert customer["lastname"] == customer_data["lastname"]
    assert customer["email"] == customer_data["email"]
    assert customer["telephone"] == customer_data["telephone"]

    delete_customer(connection, customer_id)


def test_update_customer(connection):
    customer_id = create_customer(connection, _customer_data())
    updated_data = _customer_data(
        firstname="Updated",
        lastname="Name",
        telephone="9876543210",
    )

    rowcount = update_customer(connection, customer_id, updated_data)
    assert rowcount == 1

    customer = get_customer_by_id(connection, customer_id)
    assert customer is not None
    assert customer["firstname"] == updated_data["firstname"]
    assert customer["lastname"] == updated_data["lastname"]
    assert customer["email"] == updated_data["email"]
    assert customer["telephone"] == updated_data["telephone"]

    delete_customer(connection, customer_id)


def test_update_nonexistent_customer(connection):
    nonexistent_id = 999_999_999
    rowcount = update_customer(
        connection,
        nonexistent_id,
        _customer_data(firstname="No", lastname="One"),
    )
    assert rowcount == 0


def test_delete_customer(connection):
    customer_id = create_customer(connection, _customer_data())

    rowcount = delete_customer(connection, customer_id)
    assert rowcount == 1
    assert get_customer_by_id(connection, customer_id) is None


def test_delete_nonexistent_customer(connection):
    nonexistent_id = 999_999_999
    rowcount = delete_customer(connection, nonexistent_id)
    assert rowcount == 0
