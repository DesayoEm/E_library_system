class ELibraryException(Exception):
    pass

class UserException(ELibraryException):
    """base for user related errors"""
    pass

class BookException(ELibraryException):
    """base for book related errors"""
    pass

class BorrowException(ELibraryException):
    """base for borrow and return related errors"""
    pass


class InactiveUserError(UserException):
    def __init__(self):
        super().__init__("User is inactive and cannot borrow books")

class EmailLinkedError(UserException):
    def __init__(self):
        super().__init__("This email is already linked to a library account. Please sign in with your e-mail address")

class EmailRegisteredError(UserException):
    def __init__(self):
        super().__init__("This email is already registered by another user")


class BookUnavailableError(BookException):
    def __init__(self):
        super().__init__("Book is unavailable for borrowing")


class DuplicateBookError(BookException):
    def __init__(self, book):
        self.book = book
        super().__init__(f"Book title '{book.title}' written by {book.author} already exists")


class ReturnDateError(BorrowException):
    def __init__(self):
        super().__init__("Return date cannot be earlier than borrow date")

class InvalidDateError(BorrowException):
    def __init__(self):
        super().__init__("Return date cannot be in the future")



