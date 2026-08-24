import json
import logging
import time
from typing import Any, Optional

import allure
import requests


class BookerClient:
    def __init__(self, base_url: str, timeout: int = 60) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.token: Optional[str] = None

    def close(self) -> None:
        self.session.close()

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _attach(self, response: requests.Response) -> None:
        request_body = response.request.body
        if isinstance(request_body, bytes):
            request_body = request_body.decode("utf-8", errors="replace")

        allure.attach(
            f"{response.request.method} {response.request.url}\n"
            f"Headers: {dict(response.request.headers)}\n"
            f"Body: {request_body}",
            name="request",
            attachment_type=allure.attachment_type.TEXT,
        )

        content_type = response.headers.get("Content-Type", "")
        attach_type = (
            allure.attachment_type.JSON
            if "json" in content_type
            else allure.attachment_type.TEXT
        )
        allure.attach(
            f"Status: {response.status_code}\n{response.text}",
            name="response",
            attachment_type=attach_type,
        )

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        attempts = 3
        last_error: Exception | None = None
        last_response: requests.Response | None = None

        for attempt in range(1, attempts + 1):
            try:
                self.logger.info("%s %s (attempt %s/%s)", method.upper(), path, attempt, attempts)
                response = self.session.request(method, self._url(path), **kwargs)
                last_response = response
                if response.status_code in (502, 503, 504) and attempt < attempts:
                    self.logger.warning("Got HTTP %s, retrying...", response.status_code)
                    time.sleep(2 * attempt)
                    continue
                self._attach(response)
                return response
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
                last_error = exc
                self.logger.warning("Request failed: %s", exc)
                if attempt < attempts:
                    time.sleep(2 * attempt)
                    continue
                raise

        if last_response is not None:
            self._attach(last_response)
            return last_response
        raise last_error or AssertionError("Request failed without response")

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    @allure.step("GET /ping")
    def ping(self) -> requests.Response:
        return self.get("/ping")

    @allure.step("POST /auth as {username}")
    def create_token(self, username: str = "admin", password: str = "password123") -> requests.Response:
        response = self.post("/auth", json={"username": username, "password": password})
        try:
            token = response.json().get("token")
        except json.JSONDecodeError:
            token = None
        if token:
            self.token = token
            self.session.cookies.set("token", token)
        return response

    def authenticate(self, username: str = "admin", password: str = "password123") -> str:
        response = self.create_token(username, password)
        response.raise_for_status()
        if not self.token:
            raise AssertionError(f"Auth succeeded without token: {response.text}")
        return self.token

    @allure.step("GET /booking")
    def get_booking_ids(self, **params: Any) -> requests.Response:
        return self.get("/booking", params=params or None)

    @allure.step("GET /booking/{booking_id}")
    def get_booking(self, booking_id: int) -> requests.Response:
        return self.get(f"/booking/{booking_id}")

    @allure.step("POST /booking")
    def create_booking(self, payload: dict[str, Any]) -> requests.Response:
        return self.post("/booking", json=payload)

    @allure.step("PUT /booking/{booking_id}")
    def update_booking(self, booking_id: int, payload: dict[str, Any]) -> requests.Response:
        return self.put(f"/booking/{booking_id}", json=payload)

    @allure.step("PATCH /booking/{booking_id}")
    def patch_booking(self, booking_id: int, payload: dict[str, Any]) -> requests.Response:
        return self.patch(f"/booking/{booking_id}", json=payload)

    @allure.step("DELETE /booking/{booking_id}")
    def delete_booking(self, booking_id: int) -> requests.Response:
        return self.delete(f"/booking/{booking_id}")
