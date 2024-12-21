from schemas.borrow_record_schema import BorrowRecord
from datetime import date

borrows = {
    101: BorrowRecord(
        id=101,
        user_id="2c4f6041-248d-4031-95f3-3644d9b5e1f5",
        book_id="8g9h0i1j-2k3l-4m5n-6o7p-8q9r0s1t2u3",
        borrow_date=date(2024, 12, 5),
        return_date=date(2024, 12, 13)
    ),
    102: BorrowRecord(
        id=102,
        user_id="910bd9b9-2d8a-4695-8352-cbfde21ac5ac",
        book_id="7f8g9h0i-1j2k-3l4m-5n6o-7p8q9r0s1t2",
        borrow_date=date(2024, 12, 2),
        return_date=date(2024, 12, 10)
    )
}
