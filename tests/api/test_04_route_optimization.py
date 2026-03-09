import os
from datetime import datetime, timedelta

import pytest

from tests.api.helpers import assert_ok_response


@pytest.mark.route
def test_route_plan_all_smoke(session, api_base_url):
    """Run a lightweight route-plan smoke test.

    Coordinates are taken from env when available to fit local data coverage.
    """
    start_lat = float(os.getenv("ROUTE_START_LAT", "31.2304"))
    start_lon = float(os.getenv("ROUTE_START_LON", "121.4737"))
    end_lat = float(os.getenv("ROUTE_END_LAT", "30.2741"))
    end_lon = float(os.getenv("ROUTE_END_LON", "120.1551"))

    now = datetime.utcnow()
    payload = {
        "departure_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "latest_arrival_time": (now + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S"),
        "start_lat": start_lat,
        "start_lon": start_lon,
        "end_lat": end_lat,
        "end_lon": end_lon,
        "avg_draft": 10.0,
        "sp": 12.0,
    }

    resp = session.post(f"{api_base_url}/route-optimization/plan-all", json=payload, timeout=90)
    body = assert_ok_response(resp)
    assert isinstance(body.get("data"), dict)
