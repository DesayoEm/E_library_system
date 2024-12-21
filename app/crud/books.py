from fastapi import HTTPException
from uuid import uuid4
from schemas.book_schemas import Book, NewBook, UpdateBook
from data.books import books
from typing import Dict, Optional
from services.book_services import BookService
from exceptions import DuplicateBookError

class BookCrud:
    def __init__(self, data: Dict[str, Book], book_service: BookService):
        self.book_service = BookService()
        self.books = books


    def create_book(self, new_book:NewBook) -> Book:
        try:
            self.book_service.check_duplicate_book(new_book)
        except DuplicateBookError as e:
            raise HTTPException(status_code = 409,detail = str(e))

        book_id = str(uuid4())
        created_book = Book(id = book_id, is_available = True, **new_book.model_dump())
        self.books[created_book.id] = created_book
        return created_book


    def get_books(
            self,
            author: Optional[str] = None,
            available: Optional[bool] = None,
            search: Optional[str] = None,
            skip: int = 0,
            limit: int = 50
    ) -> Dict[str, Book]:
        filtered_books = {}

        for book_id, book in self.books.items():
            matches = True

            if author and author.casefold() not in book.author.casefold():
                matches = False

            if available is not None and book.is_available != available:
                matches = False

            if search and search.casefold() not in book.title.casefold():
                matches = False

            if matches:
                filtered_books[book_id] = book

        if not filtered_books:
            raise HTTPException(status_code=404, detail="No books found matching the specified criteria")

        paginated = list(filtered_books.items())[skip:skip + limit]

        return dict(paginated)




    def get_book(self, book_id: str) -> Book:
        if book_id not in self.books:
            raise HTTPException(status_code = 404, detail = "Book not found")
        return self.books[book_id]


    def update_book(self, book_id: str, data:UpdateBook) -> Book:
        book = self.get_book(book_id)
        try:
            self.book_service.check_duplicate_book(data)
        except DuplicateBookError as e:
            raise HTTPException(status_code = 409,detail = str(e) )

        for field in ["title", "author"]:
            setattr(book, field, getattr(data, field))
        return book


    def mark_book_unavailable(self, book_id: str) -> Book:
        book = self.get_book(book_id)
        book.is_available = False
        self.books[book_id] = book
        return book


    def delete_book(self, book_id: str):
        book = self.get_book(book_id)
        del self.books[book_id]



book_crud = BookCrud(books, BookService())