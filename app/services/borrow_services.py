from crud.books import book_crud
from crud.users import user_crud

from schemas.borrow_record_schema import BorrowRecord, BorrowModel, ReturnModel
from data.borrows import borrows
from datetime import date
from exceptions import InvalidDateError, ReturnDateError, InactiveUserError, BookUnavailableError

class BorrowService:
    def __init__(self):
        self.borrows = borrows

    def validate_borrow_eligibility(self, user_id: str, book_id: str) -> None:
        user = user_crud.get_user(user_id)
        book = book_crud.get_book(book_id)

        if not user.is_active:
            raise InactiveUserError()
        if not book.is_available:
            raise BookUnavailableError()


    def generate_borrow_id(self) -> int:
        """generates id for new borrow records"""
        if not self.borrows:
            return 100
        return max(borrows.keys()) + 1


    def process_borrow_record(self, payload: BorrowModel) -> BorrowRecord:
        """generates a borrow record"""
        borrow_id = self.generate_borrow_id()
        record = BorrowRecord(
            id = borrow_id,
            user_id = payload.user_id,
            book_id = payload.book_id,
            borrow_date = date.today(),
            return_date = None
        )
        borrows[borrow_id] = record
        return record

    def get_borrow_record(self, borrow_id: int) -> BorrowRecord:
        return self.borrows.get(borrow_id)

    def validate_return_date(self, borrow_id: int, payload: ReturnModel):
        """ensures return date is not < borrow date """
        borrow = self.get_borrow_record(borrow_id)
        borrow_date=borrow.borrow_date
        return_date= payload.return_date

        if return_date < borrow_date:
            raise ReturnDateError()

        if return_date > date.today():
            raise InvalidDateError()



    def process_return(self, borrow_id: int, payload: ReturnModel) -> BorrowRecord:
        borrow = self.get_borrow_record(borrow_id)
        borrow.return_date = payload.return_date

        book_id = borrow.book_id
        book = book_crud.get_book(book_id)
        book.is_available = True
        return borrow