import json
import requests

from . import base_url, auth_headers

get_method = lambda endpoint: requests.get(
    f"{base_url}{endpoint}", headers=auth_headers
)

post_method = lambda endpoint, data={}: requests.post(
    f"{base_url}{endpoint}", headers=auth_headers, data=json.dumps(data)
)

put_method = lambda endpoint, data={}: requests.put(
    f"{base_url}{endpoint}", headers=auth_headers, data=json.dumps(data)
)


def test_project_id_vise_task():
    endpoint = "/task/project/15"
    response = get_method(endpoint)
    assert response.status_code == 404

    endpoint = "/task/project/11"
    response = get_method(endpoint)

    assert response.status_code == 401

    endpoint = "/task/project/13"
    response = get_method(endpoint)

    assert response.status_code == 200

    response_body = response.json()
    assert isinstance(response_body["data"], list)


def test_add_task():
    endpoint = "/task/add"
    data = {"project_id": "13", "title": "", "comment": ""}

    response = post_method(endpoint)
    assert response.status_code == 400

    response_body = response.json()
    assert response_body["error"] == "Please Provide Proper data"

    response = post_method(endpoint, data)
    assert response.status_code == 201

    response_body = response.json()
    assert isinstance(response_body["message"], str)


def test_update_task_status():
    data = {"status": "submitted"}
    endpoint = "/task/status/30"

    response = put_method(endpoint, data)
    assert response.status_code == 403

    endpoint = "/task/status/40"

    response = put_method(endpoint)
    assert response.status_code == 400

    response = put_method(endpoint, data)
    assert response.status_code == 200

    response_body = response.json()
    assert response_body["message"] == "Task:40 has been updated"
