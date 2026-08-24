import allure

from api.client.booker_client import BookerClient


@allure.feature("API")
@allure.story("Health")
@allure.title("GET /ping returns 201")
def test_healthcheck_ping(booker_client: BookerClient) -> None:
    response = booker_client.ping()
    assert response.status_code == 201
    assert "created" in response.text.lower()
