import allure

from api.client.booker_client import BookerClient
from api.data import unique_guest


@allure.feature("API")
@allure.story("Update booking")
@allure.title("PUT /booking/{id} replaces all fields")
def test_put_booking_updates_all_fields(auth_client: BookerClient, created_booking: dict) -> None:
    updated = unique_guest(
        firstname="PutName",
        lastname="PutLast",
        totalprice=250,
        depositpaid=False,
        additionalneeds="Late checkout",
    )
    response = auth_client.update_booking(created_booking["id"], updated)
    assert response.status_code == 200
    body = response.json()
    assert body["firstname"] == "PutName"
    assert body["lastname"] == "PutLast"
    assert body["totalprice"] == 250
    assert body["depositpaid"] is False
    assert body["additionalneeds"] == "Late checkout"


@allure.feature("API")
@allure.story("Update booking")
@allure.title("PATCH /booking/{id} updates firstname only")
def test_patch_booking_updates_firstname(auth_client: BookerClient, created_booking: dict) -> None:
    response = auth_client.patch_booking(created_booking["id"], {"firstname": "Patched"})
    assert response.status_code == 200
    body = response.json()
    assert body["firstname"] == "Patched"
    assert body["lastname"] == created_booking["payload"]["lastname"]


@allure.feature("API")
@allure.story("Update booking")
@allure.title("PUT /booking/{id} accepts Basic auth")
def test_put_booking_with_basic_auth(booker_url: str, created_booking: dict) -> None:
    client = BookerClient(booker_url)
    try:
        updated = unique_guest(firstname="BasicAuth")
        response = client.request(
            "PUT",
            f"/booking/{created_booking['id']}",
            json=updated,
            auth=("admin", "password123"),
        )
        assert response.status_code == 200
        assert response.json()["firstname"] == "BasicAuth"
    finally:
        client.close()
