from fastapi import APIRouter
from typing import Dict
from crud.borrows import borrow_crud
from schemas.borrow_record_schema import BorrowRecord, BorrowModel, ReturnModel


borrow_router = APIRouter()

@borrow_router.post("/", status_code=201)
def borrow_book(payload:BorrowModel) -> Dict:
    return borrow_crud.borrow_book(payload)

@borrow_router.get("/", status_code=200)
def get_all_borrows() :
    return borrow_crud.get_all_borrows()


@borrow_router.get("/{user_id}", status_code=200)
def get_user_borrow(user_id: str) -> list[BorrowRecord]:
    return borrow_crud.get_user_borrow(user_id)


@borrow_router.patch("/{borrow_id}", status_code= 200)
def return_book(borrow_id: int, payload:ReturnModel) -> Dict:
    return borrow_crud.return_book(borrow_id,payload)




