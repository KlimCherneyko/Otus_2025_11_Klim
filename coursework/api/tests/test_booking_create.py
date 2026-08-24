import allure
import pytest

from api.client.booker_client import BookerClient
from api.data import unique_guest


@allure.feature("API")
@allure.story("Create booking")
@allure.title("POST /booking creates a booking and returns id")
def test_create_booking_success(booker_client: BookerClient) -> None:
    payload = unique_guest()
    response = booker_client.create_booking(payload)
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["bookingid"], int)
    assert body["booking"]["firstname"] == payload["firstname"]


@allure.feature("API")
@allure.story("Create booking")
@allure.title("POST /booking response contains booking object")
def test_create_booking_response_schema(booker_client: BookerClient) -> None:
    payload = unique_guest()
    body = booker_client.create_booking(payload).json()
    assert set(body.keys()) >= {"bookingid", "booking"}
    booking = body["booking"]
    for field in ("firstname", "lastname", "totalprice", "depositpaid", "bookingdates"):
        assert field in booking


@allure.feature("API")
@allure.story("Create booking")
@pytest.mark.parametrize("price", [0, 1, 111, 9999])
def test_create_booking_with_price(booker_client: BookerClient, price: int) -> None:
    allure.dynamic.title(f"POST /booking accepts totalprice={price}")
    payload = unique_guest(totalprice=price)
    response = booker_client.create_booking(payload)
    assert response.status_code == 200
    assert response.json()["booking"]["totalprice"] == price


@allure.feature("API")
@allure.story("Create booking")
@pytest.mark.parametrize("depositpaid", [True, False])
def test_create_booking_depositpaid(booker_client: BookerClient, depositpaid: bool) -> None:
    allure.dynamic.title(f"POST /booking accepts depositpaid={depositpaid}")
    payload = unique_guest(depositpaid=depositpaid)
    response = booker_client.create_booking(payload)
    assert response.status_code == 200
    assert response.json()["booking"]["depositpaid"] is depositpaid


@allure.feature("API")
@allure.story("Create booking")
@allure.title("POST /booking works without additionalneeds")
def test_create_booking_without_additionalneeds(booker_client: BookerClient) -> None:
    payload = unique_guest()
    payload.pop("additionalneeds")
    response = booker_client.create_booking(payload)
    assert response.status_code == 200
    assert response.json()["booking"]["firstname"] == payload["firstname"]


@allure.feature("API")
@allure.story("Create booking")
@allure.title("POST /booking without firstname is rejected")
def test_create_booking_missing_firstname(booker_client: BookerClient) -> None:
    payload = unique_guest()
    payload.pop("firstname")
    response = booker_client.create_booking(payload)
    assert response.status_code != 200
