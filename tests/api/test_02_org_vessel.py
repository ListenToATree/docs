import pytest

from tests.api.helpers import assert_ok_response


@pytest.mark.regression
def test_company_list(session, api_base_url):
    resp = session.get(f"{api_base_url}/company", timeout=20)
    body = assert_ok_response(resp)
    assert isinstance(body.get("data"), list)


@pytest.mark.regression
def test_vessel_list(session, api_base_url):
    resp = session.get(f"{api_base_url}/vessel", params={"offset": 0, "limit": 5}, timeout=30)
    body = assert_ok_response(resp)
    assert isinstance(body.get("data"), list)


@pytest.mark.regression
def test_user_list_requires_auth_or_returns_data(session, api_base_url, maybe_token):
    headers = {}
    if maybe_token:
        headers["Token"] = maybe_token
    resp = session.get(f"{api_base_url}/user", headers=headers, timeout=20)
    if resp.status_code == 200:
        body = assert_ok_response(resp)
        assert isinstance(body.get("data"), list)
    else:
        # In environments where user list is protected, 401/403 is acceptable without auth.
        assert resp.status_code in (401, 403)
