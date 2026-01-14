from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

#
# def test_creat_user():
#     response = client.post(
#         "/api/v1/users",
#         headers={"X-Token": "coneofsilence"},
#         json={
#             "email": "chenmeng@12345.com",
#             "full_name": "12ssssss13",
#             "hashed_password": "sdafasdfadffawe "
#
#         },
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "email": "chenmeng@12345.com",
#         "full_name": "12ssssss13",
#         "id": 323
#     }


def test_update_user():
    response = client.put(
        f"/api/v1/users/{323}",
        headers={"X-Token": "coneofsilence"},
        json={
            "email": "chenmeng@12345.com",
            "full_name": "12ssssss13"

        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "email": "chenmeng@12345.com",
        "full_name": "12ssssss13",
        "id": 323
    }

def test_all_user():
    response = client.get(
        f"/api/v1/users/",
        headers={"X-Token": "coneofsilence"},
        params={
            "skip": 0,
            "limit": 100
        },
    )
    assert response.status_code == 200


def test_get_user():
    response = client.get(
        f"/api/v1/users/{323}",
        headers={"X-Token": "coneofsilence"},
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "email": "chenmeng@12345.com",
        "full_name": "12ssssss13",
        "id": 323
    }


#  pytest -k test_get_user -v