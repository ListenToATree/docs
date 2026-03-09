from typing import Any

import requests


def assert_ok_response(resp: requests.Response) -> dict[str, Any]:
    assert resp.status_code == 200, f"status={resp.status_code}, body={resp.text[:500]}"
    body = resp.json()
    assert str(body.get("code")) == "200", f"body={body}"
    return body
