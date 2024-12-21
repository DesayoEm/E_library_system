import pytest
from datetime import date
from schemas.book_schemas import Book
from schemas.user_schemas import User
from schemas.borrow_record_schema import BorrowRecord


@pytest.fixture
def mock_books():
    return {
        "7e76cccd": Book(
            id="7e76cccd",
            title="Becoming Nigerian",
            author="ElNathan John",
            is_available=True
        ),

        "bcf6f5f9": Book(
            id="bcf6f5f9",
            title="In My Father's Country",
            author="Adewale Maja-Pearce",
            is_available=False
        )
    }

@pytest.fixture
def mock_users():
    return {
        "5c5cbbbs": User(
            id="5c5cbbbs",
            name="Wade Wilson",
            email="deadpool@gmail.com",
            is_active=True
        ),

        "3e3eaade": User(
            id="3e3eaade",
            name="Slade Wilson",
            email="sladeboy@gmail.com",
            is_active=False
        )
    }
@pytest.fixture
def mock_borrows():
    return{
        201: BorrowRecord(
            id=201,
            user_id="7e76cccd",
            book_id="3e3eaade",
            borrow_date=date(2024, 12, 5),
            return_date=None
        ),
        202: BorrowRecord(
            id=202,
            user_id="3e3eaade",
            book_id="bcf6f5f9",
            borrow_date=date(2024, 12, 5),
            return_date=date (2024, 12, 6)
        )
    }
