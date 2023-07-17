import os
import json
import requests

base_url = os.environ.get("BASE_URL", "http://web")

MAIL = os.environ.get("USER_EMAIL", "")
PASS = os.environ.get("USER_PASSW", "")

headers = {
    "Content-Type": "application/json",
}


def get_acceess_token():
    access_token = ""
    credentials = {
        "email": MAIL,
        "upass": PASS,
    }
    print("get_acceess_token", base_url, credentials)
    response = requests.post(
        f"{base_url}/user/signin", headers=headers, data=json.dumps(credentials)
    )

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens["access"]

    return access_token


auth_headers = {**headers, "Authorization": f"Bearer {get_acceess_token()}"}
