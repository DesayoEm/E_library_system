from fastapi import HTTPException
import pytest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from crud.borrows import BorrowCrud
from main import app
from services.borrow_services import BorrowService
from test.mock_data import mock_borrows, mock_books


client = TestClient(app)

@pytest.fixture
def mock_borrow_service():
    return Mock(spec = BorrowService)


@pytest.fixture
def mock_borrow_crud(mock_borrow_service, mock_book_crud):
    crud = BorrowCrud(borrow_service = mock_borrow_service, book_crud=mock_book_crud)
    with patch('crud.borrows.borrow_crud', crud):
        yield crud




"""
 - Test GET all borrow records successfully
"""
def test_get_all_borrows(mock_borrows):
    with patch('routes.borrow_routes.borrow_crud.get_all_borrows', return_value = mock_borrows):
        response = client.get("/v1/borrows")
        expected_data= {
            str(borrow_id): borrow.model_dump(mode = 'json') for  borrow_id, borrow in mock_borrows.items()
        }
        assert response.status_code == 200
        assert response.json() == expected_data


"""
 - Test GET a user's borrow records successfully
"""
def test_get_user_borrows(mock_borrows):
    user_id = "7e76cccd"

    user_borrows = [
        borrow.model_dump(mode='json')
        for borrow in mock_borrows.values()
        if borrow.user_id == user_id
    ]

    with patch ('routes.borrow_routes.borrow_crud.get_user_borrow',return_value = user_borrows):
        response = client.get(f"/v1/borrows/{user_id}")
    assert response.status_code == 200
    assert response.json() == user_borrows


"""
 - Test POST borrow a book 
"""
def test_borrow_book():
    payload = {
        "user_id": "5c5cbbbs",
        "book_id": "7e76cccd",
        "borrow_date": "2024-12-18"
    }

    expected_response = {
        "borrow_id": 203,
        "user_id": payload["user_id"],
        "book_id": payload["book_id"],
        "borrow_date": payload["borrow_date"],
        "return_date": None
    }
    with patch('routes.borrow_routes.borrow_crud.borrow_book',return_value = expected_response):
        response = client.post("/v1/borrows", json=payload)
        assert response.status_code == 201
        assert response.json()["borrow_date"] == payload["borrow_date"]
        assert response.json()["return_date"] is None


"""
 - Test POST borrow a book by inactive user
"""
def test_borrow_book_inactive_user():
    payload = {
        "user_id": "3e3eaade",
        "book_id": "7e76cccd",
        "borrow_date": "2024-12-18"
    }
    with patch('routes.borrow_routes.borrow_crud.borrow_book',
               side_effect = HTTPException(status_code = 403,
                                           detail = "User is inactive and cannot borrow books")):

        response = client.post("/v1/borrows", json=payload)
        assert response.status_code == 403
        assert response.json()["detail"] == "User is inactive and cannot borrow books"


"""
 - Test POST borrow an unavailable book
"""
def test_borrow_unavailable_book():
    payload = {
        "user_id": "7e76cccd",
        "book_id": "bcf6f5f9",
        "borrow_date": "2024-12-18"
    }
    with patch('routes.borrow_routes.borrow_crud.borrow_book',
               side_effect = HTTPException(status_code = 409,
                                           detail = "Book is unavailable for borrowing")):

        response = client.post("/v1/borrows", json=payload)
        assert response.status_code == 409
        assert response.json()["detail"] == "Book is unavailable for borrowing"


"""
 - Test POST return a book successfully
"""
def test_return_book():
    payload = {
        "return_date": "2024-12-18"
    }

    borrow_id = 201
    expected_response = {
        "id": borrow_id,
        "user_id":"7e76cccd",
        "book_id":"3e3eaade",
        "borrow_date":"2024-12-5",
        "return_date":payload["return_date"]
        }
    with patch('routes.borrow_routes.borrow_crud.return_book',return_value = expected_response):

        response = client.patch(f"/v1/borrows/{borrow_id}", json=payload)
        assert response.status_code == 200
        assert response.json()["return_date"] == payload["return_date"]



"""
 - Test POST return a book with invalid date
"""
def test_return_book_invalid_date():
    payload = {
        "return_date": "2024-12-01" #date b4 borrow date
    }
    borrow_id = 201
    with patch('routes.borrow_routes.borrow_crud.return_book',
               side_effect = HTTPException(status_code = 400,
                                           detail = "Return date cannot be before borrow date")):

        response = client.patch(f"/v1/borrows/{borrow_id}", json=payload)
        assert response.status_code == 400
        assert response.json()["detail"] == "Return date cannot be before borrow date"


"""
 - Test POST return a book with invalid date
"""
def test_return_book_future_date():
    payload = {
        "return_date": "2025-12-01" #future date
    }
    borrow_id = 201
    with patch('routes.borrow_routes.borrow_crud.return_book',
               side_effect = HTTPException(status_code = 400,
                                           detail = "Return date cannot be in the future")):

        response = client.patch(f"/v1/borrows/{borrow_id}", json=payload)
        assert response.status_code == 400
        assert response.json()["detail"] == "Return date cannot be in the future"