import urllib.parse


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Basic sanity
    assert "Soccer Team" in data


def test_signup_and_unregister(client):
    activity = "Soccer Team"
    email = "teststudent@mergington.edu"

    # ensure not present
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email not in resp.json()[activity]["participants"]

    # signup
    resp = client.post(
        f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    )
    assert resp.status_code == 200
    assert f"Signed up {email}" in resp.json()["message"]

    # duplicate signup returns 400
    resp = client.post(
        f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    )
    assert resp.status_code == 400

    # unregister
    resp = client.delete(
        f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    )
    assert resp.status_code == 200
    assert f"Removed {email}" in resp.json()["message"]

    # unregister again -> 404
    resp = client.delete(
        f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    )
    assert resp.status_code == 404
