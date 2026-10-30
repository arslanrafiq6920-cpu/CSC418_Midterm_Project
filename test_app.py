import pytest
from app import app, submissions

@pytest.fixture(autouse=True)
def clear_submissions():
    submissions.clear()
    yield
    submissions.clear()

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def complete_form():
    return {
        "name": "Ali Student",
        "registration_number": "FA24-ABC-001",
        "assignment_title": "Operating Systems Lab",
        "submission_url": "https://example.com/assignment"
    }

def test_valid_submission_is_saved_and_displayed(client):
    response = client.post("/", data=complete_form())
    assert response.status_code == 200
    assert b"submitted successfully" in response.data
    assert len(submissions) == 1
    assert b"FA24-ABC-001" in response.data

def test_missing_registration_number_is_rejected(client):
    data = complete_form()
    data["registration_number"] = ""
    response = client.post("/", data=data)
    assert b"complete all required fields" in response.data
    assert len(submissions) == 0

def test_invalid_submission_url_is_rejected_and_not_saved(client):
    data = complete_form()
    data["submission_url"] = "not-a-url"
    response = client.post("/", data=data)
    assert b"valid http" in response.data
    assert len(submissions) == 0
