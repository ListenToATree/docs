import os

import pytest

from tests.api.helpers import assert_ok_response


def _get_vessel_id() -> int:
    return int(os.getenv("API_TEST_VESSEL_ID", "1"))


@pytest.mark.regression
def test_statistic_cii(session, api_base_url):
    vessel_id = _get_vessel_id()
    resp = session.get(f"{api_base_url}/statistic/vessel/{vessel_id}/cii", timeout=30)
    body = assert_ok_response(resp)
    assert isinstance(body.get("data"), list)


@pytest.mark.regression
def test_statistic_completeness(session, api_base_url):
    vessel_id = _get_vessel_id()
    resp = session.get(f"{api_base_url}/statistic/vessel/{vessel_id}/completeness", timeout=30)
    body = assert_ok_response(resp)
    assert isinstance(body.get("data"), list)


@pytest.mark.regression
def test_reminder_values(session, api_base_url):
    vessel_id = _get_vessel_id()
    resp = session.get(f"{api_base_url}/reminder/{vessel_id}/values", timeout=30)
    body = assert_ok_response(resp)
    assert isinstance(body.get("data"), dict)


@pytest.mark.calc
def test_calculate_cii(session, api_base_url):
    payload = {
        "ship_type": "I004",
        "capacity": 50000,
        "year": 2024,
        "distance": 12000,
        "fuel_consumption": [{"fuel_type": "hfo", "amount": 1200}],
    }
    resp = session.post(f"{api_base_url}/calculate/cii", json=payload, timeout=30)
    body = assert_ok_response(resp)
    assert isinstance(body.get("data"), dict)
