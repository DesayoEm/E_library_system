from fastapi import APIRouter, Query
from crud.books import book_crud
from schemas.book_schemas import NewBook, UpdateBook, Book
from typing import Dict, Optional

book_router = APIRouter()

@book_router.post("/", status_code=201)
def create_book(new_book: NewBook) -> Book:
    return book_crud.create_book(new_book)


@book_router.get("/", status_code=200)
def get_books(
        author: Optional[str] = Query(None, description="Author's name e.g 'Chinua Achebe'"),
        available: Optional[bool] = Query(None, description="Is it available?"),
        search: Optional[str] = Query(None, description="Book name e.g 'Clean Code'"),
        skip: int = Query(0, ge=0, description=""),
        limit: int = Query(10, ge=1, le=20, description="")
) -> Dict[str, Book]:

    return book_crud.get_books(
        author=author,
        available=available,
        search=search,
        skip=skip,
        limit=limit
    )


@book_router.get("/{book_id}", status_code=200)
def get_book(book_id) -> Book:
    return book_crud.get_book(book_id)


@book_router.put("/{book_id}", status_code=200)
def update_book(book_id: str, data: UpdateBook) -> Book:
    return book_crud.update_book(book_id, data)


@book_router.patch("/{book_id}", status_code=200)
def mark_book_unavailable(book_id: str) -> Book:
    return book_crud.mark_book_unavailable(book_id)


@book_router.delete("/{book_id}", status_code=204)
def delete_book(book_id: str) -> None:
    return book_crud.delete_book(book_id)

