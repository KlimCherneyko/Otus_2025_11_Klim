import uuid
from typing import Any


def unique_guest(**overrides: Any) -> dict[str, Any]:
    suffix = uuid.uuid4().hex[:8]
    payload = {
        "firstname": f"Auto{suffix}",
        "lastname": f"Tester{suffix}",
        "totalprice": 120,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-09-01",
            "checkout": "2026-09-05",
        },
        "additionalneeds": "Breakfast",
    }
    payload.update(overrides)
    return payload
