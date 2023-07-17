import requests
import json
# import os

# base_url = os.environ.get("BASE_URL", "http://web:5000")  # "docker-flask_default:5000"
from . import base_url

def test_root_url():
    print(base_url)
    response = requests.get(base_url)
    response_body = response.json()
    assert (
        response.status_code == 200
        and response_body["message"] == "Welcome to docker-flask"
    )


def test_error_signup_password_url():
    response = requests.post(
        f"{base_url}/user/signup",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {"email": "test.py@gmail.com", "uname": "Py Test", "upass": "py123"}
        ),
    )
    assert response.status_code == 406
    response_body = response.json()
    assert response_body["error"]


def test_error_signup_exists_url():
    response = requests.post(
        f"{base_url}/user/signup",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "email": "Jigar.vakil@gmail.com",
                "uname": "Jigar Vakil",
                "upass": "JVakil",
            }
        ),
    )
    assert response.status_code == 403

    response_body = response.json()
    assert response_body["error"] == "Email already exists"


def test_error_signin_exists_url():
    response = requests.post(
        f"{base_url}/user/signin",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"email": "test.py@gmail.com", "upass": "py123"}),
    )
    assert response.status_code == 404
    response_body = response.json()
    assert response_body["error"] == "No User Found"


def test_error_signin_invalid_url():
    response = requests.post(
        f"{base_url}/user/signin",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"email": "Jigar.vakil@gmail.com", "upass": "Jkil"}),
    )
    assert response.status_code == 403
    response_body = response.json()
    assert response_body["error"] == "Credentials are invalid"
