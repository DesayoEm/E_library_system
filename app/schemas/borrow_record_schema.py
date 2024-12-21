from pydantic import BaseModel, field_validator, Field
from datetime import date, datetime
from typing import Any
from dateutil.parser import parse


class BorrowModel(BaseModel):
    user_id: str
    book_id: str

    model_config = {
        "json_schema_extra":{
            "example": {
                "user_id": "2c4f6041-248d-4031-95f3-3644d9b5e1f5",
                "book_id": "9h0i1j2k-3l4m-5n6o-7p8q-9r0s1t2u3v4",
            }
        }
    }
class Borrow(BorrowModel):
    id:int
    borrow_date: date = Field(
        description = "The date the book was borrowed. System generated and defaults to the date of the operation" ,
        examples = ["2024-12-15"]
    )

class BorrowRecord(Borrow):
    return_date: date | None = None


class ReturnModel(BaseModel):
    return_date:str | date = Field(
        description = "The date the book was returned. Has to be a past or present date ans has to be >= borrow date" ,
        examples = ["2024-12-15"]
    )
    model_config = {
         "json_schema_extra":{
             "return_date": "2024-12-10"
         }
     }

    @field_validator("return_date", mode="before")
    def parse_return_date(cls, value:Any) -> date:
        """convert string date to a date objects"""
        if isinstance(value, date):
            return value

        if isinstance (value, str):
            try:
                return parse(value).date()
            except ValueError:
                raise ValueError("Return date must be a valid date string or date object")
        return value





