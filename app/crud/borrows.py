from fastapi import HTTPException
from typing import Dict
from schemas.borrow_record_schema import BorrowRecord, BorrowModel, ReturnModel
from data.borrows import borrows
from services.book_services import BookService
from services.borrow_services import BorrowService
from crud.users import user_crud
from crud.books import book_crud, BookCrud
from exceptions import ReturnDateError, InactiveUserError, BookUnavailableError, InvalidDateError


class BorrowCrud:
    def __init__(self, borrow_service: BorrowService, book_crud: BookCrud):
        self.borrow_service = borrow_service
        self.borrows = borrows
        self.book_crud = book_crud


    def get_all_borrows(self) -> Dict[int, BorrowRecord]:
        return self.borrows


    def get_user_borrow(self, user_id) -> list[BorrowRecord]:
        user = user_crud.get_user(user_id)
        user_borrows =  [borrow for borrow in self.borrows.values() if user.id == borrow.user_id]
        if not user_borrows:
            raise HTTPException(status_code=404, detail= "User has no borrows!")
        return user_borrows


    def borrow_book(self, payload:BorrowModel) -> Dict:
        try:
            self.borrow_service.validate_borrow_eligibility(payload.user_id, payload.book_id)
        except InactiveUserError as e:
            raise HTTPException (status_code=403, detail = str(e))
        except BookUnavailableError as e:
            raise HTTPException (status_code=409, detail = str(e))

        borrow_record = self.borrow_service.process_borrow_record(payload)
        self.book_crud.mark_book_unavailable(payload.book_id)

        return borrow_record.model_dump(exclude=["user_id", "book_id"])


    def return_book(self, borrow_id: int, payload:ReturnModel) -> Dict:
        borrow_record = self.borrows.get(borrow_id)
        if not borrow_record:
            raise HTTPException(status_code=404, detail="Borrow record not found")

        try:
            self.borrow_service.validate_return_date(borrow_id, payload)
        except ReturnDateError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except InvalidDateError as e:
            raise HTTPException(status_code=400, detail=str(e))


        processed_return = self.borrow_service.process_return(borrow_id, payload)
        return processed_return.model_dump(exclude=["user_id", "book_id"])

borrow_crud = BorrowCrud(BorrowService(), book_crud)