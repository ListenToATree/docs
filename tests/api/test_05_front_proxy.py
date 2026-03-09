import pytest
import os


def _front_checks_enabled() -> bool:
    return os.getenv("RUN_FRONT_PROXY_TESTS", "0") == "1"


@pytest.mark.smoke
def test_front_proxy_root(session, front_base_url):
    if not _front_checks_enabled():
        pytest.skip("set RUN_FRONT_PROXY_TESTS=1 to enable frontend proxy checks")
    resp = session.get(f"{front_base_url}/", timeout=20)
    assert resp.status_code in (200, 304)


@pytest.mark.smoke
def test_front_proxy_api_bridge(session, front_base_url):
    if not _front_checks_enabled():
        pytest.skip("set RUN_FRONT_PROXY_TESTS=1 to enable frontend proxy checks")
    resp = session.get(f"{front_base_url}/api/", timeout=20)
    assert resp.status_code == 200
    body = resp.json()
    assert str(body.get("code")) == "200"
