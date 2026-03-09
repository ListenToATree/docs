import os
from typing import Any

import pytest
import requests


BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:18000").rstrip("/")
FRONT_BASE_URL = os.getenv("FRONT_BASE_URL", "http://127.0.0.1:5173").rstrip("/")


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def front_base_url() -> str:
    return FRONT_BASE_URL


@pytest.fixture(scope="session")
def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    return s


@pytest.fixture(scope="session")
def test_user_payload() -> dict[str, Any]:
    return {
        "username": os.getenv("API_TEST_USERNAME", ""),
        "password": os.getenv("API_TEST_PASSWORD", ""),
    }


@pytest.fixture(scope="session")
def maybe_token(
    session: requests.Session,
    api_base_url: str,
    test_user_payload: dict[str, Any],
) -> str | None:
    """Login when credentials are provided; otherwise return None.

    This keeps the suite executable in both anonymous and authenticated modes.
    """
    if not test_user_payload["username"] or not test_user_payload["password"]:
        return None

    resp = session.post(f"{api_base_url}/user/login", json=test_user_payload, timeout=20)
    if resp.status_code != 200:
        return None

    data = resp.json()
    token = (data.get("data") or {}).get("token")
    return token


def assert_ok_response(resp: requests.Response) -> dict[str, Any]:
    assert resp.status_code == 200, f"status={resp.status_code}, body={resp.text[:500]}"
    body = resp.json()
    assert str(body.get("code")) == "200", f"body={body}"
    return body
