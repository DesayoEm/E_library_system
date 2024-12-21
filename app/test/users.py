import pytest
from main import app
from fastapi import HTTPException
from schemas.user_schemas import User
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from uuid import uuid4
from crud.users import UserCrud
from services.user_services import UserService
from test.mock_data import mock_users


client = TestClient(app)

@pytest.fixture
def mock_user_service():
    return Mock(spec=UserService)

@pytest.fixture
def mock_user_crud(mock_users, mock_user_service):
    crud = UserCrud(data=mock_users, user_service=mock_user_service)
    with patch('crud.users.user_crud', crud):
        yield crud


def test_get_users(mock_users):
    with patch('routes.user_routes.user_crud.get_all_users', return_value=mock_users):
        response = client.get("/v1/users")
        expected_data = {id_: user.model_dump() for id_, user in mock_users.items()}

        assert response.status_code == 200
        assert response.json() == expected_data

"""
 - Test GET a user successfully
"""
def test_get_user(mock_users):
    user_id = "5c5cbbbs"
    with patch('routes.user_routes.user_crud.get_user',return_value=mock_users[user_id]):

        response = client.get(f"/v1/users/{user_id}")

        assert response.status_code == 200
        assert response.json() ==  mock_users[user_id].model_dump()


"""
 - Test GET a nonexistent user and 404 error msg.
"""
def test_get_user_not_found():
    user_id = "0000000"
    with patch('routes.user_routes.user_crud.get_user',
               side_effect=HTTPException(status_code=404, detail="User not found")):
        response = client.get(f"/v1/users/{user_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"


"""
 - Test POST new user 
"""
def test_create_user():
    payload = {
        "name": "Roy Harper",
        "email": "arsenal@yahoo.com",
         }

    expected_user = User(
        id = str(uuid4()),
        name=payload["name"],
        email=payload["email"],
        is_active=True
         )
    with patch('routes.user_routes.user_crud.create_user', return_value = expected_user.model_dump()):

        response = client.post("/v1/users", json = payload)
        new_user = User(**response.json())

        assert response.status_code == 201
        assert expected_user == new_user


"""
 - Test POST new user with duplicate email
"""
def test_create_duplicate_user():
    payload = {
        "name": "Wade Wilson",
        "email": "deadpool@gmail.com",
    }

    with patch('routes.user_routes.user_crud.create_user',
               side_effect=HTTPException(status_code=409,
                detail="This email is already linked to a library account. Please sign in with your e-mail address")):

        response = client.post("/v1/users", json = payload)
        assert response.status_code == 409
        assert response.json()["detail"] == "This email is already linked to a library account. Please sign in with your e-mail address"


"""
 - Test PUT user 
"""
def test_update_user():
    payload = {
        "name": "Updated user",
        "email": "uparsenal@yahoo.com",
       }
    user_id = "5c5cbbbs"
    expected_response = User(
        id = user_id,
        name=payload["name"],
        email=payload["email"],
        is_active=True
    )
    with patch('routes.user_routes.user_crud.update_user', return_value = expected_response.model_dump()):
        response = client.put(f"/v1/users/{user_id}", json = payload)
        assert response.status_code == 200
        assert response.json()["name"] == "Updated user"
        assert response.json()["email"] == "uparsenal@yahoo.com"


"""
 - Test PUT user with duplicate email
"""
def test_update_user_with_duplicate_email():
    payload = {
        "name": "Updated user",
        "email": "sladeboy@gmail.com",
    }
    with patch('routes.user_routes.user_crud.update_user',
               side_effect=HTTPException(status_code=409,
                                         detail='This email is already registered by another user')):
        response = client.put("/v1/users/5c5cbbbs", json = payload)
        assert response.status_code == 409
        assert response.json()["detail"] == "This email is already registered by another user"


"""
 - Test PATCH deactivate user
"""
def test_deactivate_user(mock_users):
    user_id = "5c5cbbbs"
    deactivated_user = mock_users[user_id]
    deactivated_user.is_active = False

    with patch('routes.user_routes.user_crud.deactivate_user',return_value = mock_users[user_id]):
        response = client.patch(f"/v1/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["is_active"] == False
        assert mock_users[user_id].is_active == False


"""
 - Test DELETE user
"""
def test_delete_user(mock_users):
    user_id = "5c5cbbbs"

    with patch('routes.user_routes.user_crud.delete_user',return_value=None):
        response=client.delete(f"/v1/users/{user_id}")
        assert response.status_code == 204

