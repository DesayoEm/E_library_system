import pytest
from main import app
from fastapi import HTTPException
from schemas.book_schemas import Book
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from crud.books import BookCrud
from services.book_services import BookService
from test.mock_data import mock_books
from uuid import uuid4



client = TestClient(app)

@pytest.fixture
def mock_book_service():
    return Mock(spec = BookService)

@pytest.fixture
def mock_book_crud(mock_books, mock_book_service):
    crud = BookCrud(data=mock_books, book_service=mock_book_service)
    with patch('crud.books.book_crud', crud):
        yield crud


"""
 - Test GET all books successfully
"""

def test_get_books(mock_books):
    with patch('routes.book_routes.book_crud.get_books', return_value = mock_books):
        response = client.get("/v1/books")
        expected_data= {
            book_id: book.model_dump() for book_id, book in mock_books.items()
        }
        assert response.status_code == 200
        assert response.json() == expected_data


"""
 - Test GET a book successfully
"""
def test_book(mock_books):
    book_id = "bcf6f5f9"
    with patch('routes.book_routes.book_crud.get_book', return_value = mock_books[book_id]):
        response = client.get(f"/v1/books/{book_id}")
        assert response.status_code == 200
        assert response.json() ==  mock_books[book_id].model_dump()


"""
 - Test GET a nonexistent book and 404 error msg.
"""

def test_book_not_found():
    with patch('routes.book_routes.book_crud.get_book',
               side_effect = HTTPException(status_code=404, detail="Book not found")):
        nonexistent_id = "2222222"
        response = client.get(f"/v1/books/{nonexistent_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Book not found"


"""
 - Test POST new book
"""
def test_create_book():
    payload = {
        "author": "Cyprian Ekwensi",
        "title": "Burning Grass"
    }

    expected_book = Book(
        id = str(uuid4()),
        title=payload["title"],
        author=payload["author"],
        is_available=True
    )

    with patch('routes.book_routes.book_crud.create_book', return_value = expected_book):
        response = client.post("/v1/books", json = payload)
        new_book = Book(**response.json())

        assert response.status_code == 201
        assert expected_book == new_book



"""
 - Test POST duplicate book
"""

def test_create_duplicate_book():
    payload = {
        "author": "ElNathan John",
        "title": "Becoming Nigerian"
    }
    with patch('routes.book_routes.book_crud.create_book',
               side_effect = HTTPException(status_code = 409,
                                           detail = f"""Book title '{payload["title"]}' written by {payload["author"]} already exists""")):
        response = client.post("/v1/books", json = payload)
        assert response.status_code == 409
        assert response.json()["detail"] == "Book title 'Becoming Nigerian' written by ElNathan John already exists"


"""
 - Test PUT book 
"""
def test_update_book(mock_books):
    payload = {
        "author": "Chimamanda Adichie",
        "title": "Half Of A Yellow Sun"
    }
    book_id = "7e76cccd"
    updated_book = Book(
        id = book_id,
        title=payload["title"],
        author=payload["author"],
        is_available=True
    )
    with patch('routes.book_routes.book_crud.update_book', return_value = updated_book):
        response = client.put("/v1/books/7e76cccd", json = payload)
        assert response.status_code == 200
        assert response.json()["author"] == payload["author"]
        assert response.json()["title"] == payload["title"]


"""
 - Test PUT duplicate book
"""
def test_update_duplicate_book():
    payload = {
        "author": "Adewale Maja-Pearce",
        "title": "In My Father's Country"
    }
    book_id = "7e76cccd"
    with patch('routes.book_routes.book_crud.update_book',
               side_effect = HTTPException(status_code=409,
                                           detail=f"""Book title '{payload["title"]}' written by {payload["author"]} already exists""")):
        response = client.put(f"/v1/books/{book_id}", json = payload)
        assert response.status_code == 409
        assert response.json()["detail"] == f"""Book title 'In My Father's Country' written by Adewale Maja-Pearce already exists"""


"""
 - Test PATCH deactivate book
"""
def test_deactivate_book(mock_books):
    book_id = "7e76cccd"
    deactivated_book = mock_books[book_id]
    deactivated_book.is_available = False

    with patch('routes.book_routes.book_crud.mark_book_unavailable', return_value = mock_books[book_id]):
        response = client.patch(f"/v1/books/{book_id}")
        assert response.status_code == 200
        assert mock_books[book_id].is_available == False


"""
 - Test DELETE book
"""

def test_delete_book():
    book_id = "7e76cccd"

    with patch('routes.book_routes.book_crud.delete_book',return_value = None):
        response=client.delete(f"/v1/books/{book_id}")
        assert response.status_code == 204

