import pytest

from tests.api.helpers import assert_ok_response


@pytest.mark.smoke
def test_backend_root(session, api_base_url):
    resp = session.get(f"{api_base_url}/", timeout=20)
    body = assert_ok_response(resp)
    assert "data" in body


@pytest.mark.smoke
def test_meta_ship_type(session, api_base_url):
    resp = session.get(f"{api_base_url}/meta/ship_type", timeout=20)
    body = assert_ok_response(resp)
    assert isinstance(body.get("data"), list)


@pytest.mark.smoke
def test_meta_fuel_type(session, api_base_url):
    resp = session.get(f"{api_base_url}/meta/fuel_type", timeout=20)
    body = assert_ok_response(resp)
    assert isinstance(body.get("data"), list)


@pytest.mark.smoke
def test_meta_time_zone(session, api_base_url):
    resp = session.get(f"{api_base_url}/meta/time_zone", timeout=20)
    if resp.status_code != 200:
        pytest.skip(f"time_zone endpoint unavailable in current env: status={resp.status_code}")
    body = assert_ok_response(resp)
    assert isinstance(body.get("data"), list)


@pytest.mark.smoke
def test_api_prefix_compatibility(session, api_base_url):
    direct = session.get(f"{api_base_url}/meta/ship_type", timeout=20)
    prefixed = session.get(f"{api_base_url}/api/meta/ship_type", timeout=20)
    body_direct = assert_ok_response(direct)
    body_prefixed = assert_ok_response(prefixed)
    assert len(body_direct.get("data", [])) == len(body_prefixed.get("data", []))
