import time

import pytest

from api.client.booker_client import BookerClient
from api.data import unique_guest


@pytest.fixture(scope="session", autouse=True)
def warmup_booker(booker_url: str) -> None:
    client = BookerClient(booker_url, timeout=60)
    try:
        for _ in range(5):
            try:
                if client.ping().status_code == 201:
                    return
            except Exception:
                time.sleep(3)
    finally:
        client.close()


@pytest.fixture()
def booker_client(booker_url: str) -> BookerClient:
    client = BookerClient(booker_url)
    yield client
    client.close()


@pytest.fixture()
def auth_client(booker_url: str) -> BookerClient:
    client = BookerClient(booker_url)
    client.authenticate()
    yield client
    client.close()


@pytest.fixture()
def created_booking(booker_client: BookerClient) -> dict:
    payload = unique_guest()
    response = None
    for _ in range(3):
        response = booker_client.create_booking(payload)
        if response.status_code == 200:
            body = response.json()
            return {"id": body["bookingid"], "payload": payload, "response": body}
        time.sleep(2)
    assert response is not None and response.status_code == 200, getattr(response, "text", "")
