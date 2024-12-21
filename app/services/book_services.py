from schemas.book_schemas import NewBook
from data.books import books
from exceptions import DuplicateBookError

class BookService:
    def __init__(self):
        self.books = books

    def check_duplicate_book(self, new_book: NewBook):
        duplicate_book = any(
                book.title.casefold() == new_book.title.casefold()
                and book.author.casefold() == new_book.author.casefold()
                for book in self.books.values()
            )
        if duplicate_book:
            raise DuplicateBookError(new_book)