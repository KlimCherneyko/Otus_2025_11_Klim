import allure
import pytest

from api.client.booker_client import BookerClient
from api.data import unique_guest


@allure.feature("API")
@allure.story("Authentication")
@allure.title("POST /auth returns a token for valid credentials")
def test_create_token_valid_credentials(booker_client: BookerClient) -> None:
    response = booker_client.create_token()
    assert response.status_code == 200
    body = response.json()
    assert "token" in body
    assert isinstance(body["token"], str)
    assert body["token"]


@allure.feature("API")
@allure.story("Authentication")
@pytest.mark.parametrize(
    "username, password",
    [
        ("admin", "wrong"),
        ("admin", ""),
        ("unknown", "password123"),
    ],
)
def test_create_token_invalid_credentials(
    booker_client: BookerClient,
    username: str,
    password: str,
) -> None:
    allure.dynamic.title(f"POST /auth rejects {username!r} / {password!r}")
    response = booker_client.create_token(username=username, password=password)
    assert response.status_code == 200
    body = response.json()
    assert "token" not in body
    assert "reason" in body


@allure.feature("API")
@allure.story("Authentication")
@allure.title("PUT /booking/{id} without token is forbidden")
def test_update_without_auth_returns_forbidden(
    booker_client: BookerClient,
    created_booking: dict,
) -> None:
    response = booker_client.update_booking(created_booking["id"], unique_guest())
    assert response.status_code == 403
