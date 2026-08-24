import allure
import pytest

from api.client.booker_client import BookerClient


@allure.feature("API")
@allure.story("Read booking")
@allure.title("GET /booking returns a list of booking ids")
def test_get_all_booking_ids(booker_client: BookerClient) -> None:
    response = booker_client.get_booking_ids()
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert body
    assert "bookingid" in body[0]


@allure.feature("API")
@allure.story("Read booking")
@allure.title("GET /booking/{id} returns the created booking")
def test_get_booking_by_id(booker_client: BookerClient, created_booking: dict) -> None:
    response = booker_client.get_booking(created_booking["id"])
    assert response.status_code == 200
    body = response.json()
    payload = created_booking["payload"]
    assert body["firstname"] == payload["firstname"]
    assert body["lastname"] == payload["lastname"]
    assert body["totalprice"] == payload["totalprice"]
    assert body["depositpaid"] == payload["depositpaid"]
    assert body["bookingdates"] == payload["bookingdates"]
    assert body["additionalneeds"] == payload["additionalneeds"]


@allure.feature("API")
@allure.story("Read booking")
@allure.title("GET /booking/{id} returns 404 for unknown id")
def test_get_booking_not_found(booker_client: BookerClient) -> None:
    response = booker_client.get_booking(99999999)
    assert response.status_code == 404


@allure.feature("API")
@allure.story("Read booking")
@pytest.mark.parametrize("filter_key", ["firstname", "lastname"])
def test_filter_booking_by_name(
    booker_client: BookerClient,
    created_booking: dict,
    filter_key: str,
) -> None:
    value = created_booking["payload"][filter_key]
    allure.dynamic.title(f"GET /booking filters by {filter_key}")
    response = booker_client.get_booking_ids(**{filter_key: value})
    assert response.status_code == 200
    ids = [item["bookingid"] for item in response.json()]
    assert created_booking["id"] in ids


@allure.feature("API")
@allure.story("Read booking")
@allure.title("GET /booking filters by checkin date")
def test_filter_booking_by_checkin_date(
    booker_client: BookerClient,
    created_booking: dict,
) -> None:
    response = booker_client.get_booking_ids(checkin="2026-08-01")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert all("bookingid" in item for item in body)
    assert created_booking["id"] in [item["bookingid"] for item in body]


@allure.feature("API")
@allure.story("Read booking")
@allure.title("GET /booking/{id} response has expected field types")
def test_get_booking_field_types(booker_client: BookerClient, created_booking: dict) -> None:
    body = booker_client.get_booking(created_booking["id"]).json()
    assert isinstance(body["firstname"], str)
    assert isinstance(body["lastname"], str)
    assert isinstance(body["totalprice"], int)
    assert isinstance(body["depositpaid"], bool)
    assert isinstance(body["bookingdates"], dict)
    assert isinstance(body["bookingdates"]["checkin"], str)
    assert isinstance(body["bookingdates"]["checkout"], str)
