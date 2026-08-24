import allure

from api.client.booker_client import BookerClient


@allure.feature("API")
@allure.story("Delete booking")
@allure.title("DELETE /booking/{id} removes the booking")
def test_delete_booking_success(auth_client: BookerClient, created_booking: dict) -> None:
    response = auth_client.delete_booking(created_booking["id"])
    assert response.status_code == 201


@allure.feature("API")
@allure.story("Delete booking")
@allure.title("GET /booking/{id} returns 404 after delete")
def test_deleted_booking_not_found(auth_client: BookerClient, created_booking: dict) -> None:
    delete_response = auth_client.delete_booking(created_booking["id"])
    assert delete_response.status_code == 201
    get_response = auth_client.get_booking(created_booking["id"])
    assert get_response.status_code == 404


@allure.feature("API")
@allure.story("Delete booking")
@allure.title("DELETE /booking/{id} without token is forbidden")
def test_delete_booking_without_auth(booker_client: BookerClient, created_booking: dict) -> None:
    response = booker_client.delete_booking(created_booking["id"])
    assert response.status_code == 403
