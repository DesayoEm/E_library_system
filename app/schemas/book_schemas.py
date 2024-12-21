from pydantic import BaseModel, field_validator, Field
from typing import Optional

class NewBook(BaseModel):
    """Base model for creating new book."""
    title: str = Field (
       description = "The book's title" ,
       examples = ["A Mind For Numbers"]
    )
    author: str = Field (
        description = "The full name of the author",
        examples = ["Barbara Oakley"]
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A Mind For Numbers",
                "author": "Barbara Oakley"
            }
        }}


    @field_validator('title')
    def validate_title(cls,value):
        """validates and formats the book title."""
        if len(value) < 2:
            raise ValueError("Book title must be greater than one character")
        if value.isspace():
            raise ValueError("Book name cannot be whitespace")
        return value


    @field_validator('author')
    def validate_author_name(cls,value):
        """validates author's name format."""
        if len(value) < 2:
            raise ValueError("Author's name must be greater than one character")
        if  any(char.isdigit() for char in value):
            raise ValueError("Author's name cannot contain a digit")
        if value.isspace():
            raise ValueError("Author's name cannot be whitespace")
        return value


class Book(NewBook):
    """
    complete book model with `id` and `status`.
    Inherits validators and the `title` and `author` fields from `NewBook`
    """
    id: str = Field(
        description="Automatically generated unique identifier for the book in UUID format",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )

    is_available: bool = Field(
        default=True,
        description="Indicates if the book is currently available for borrowing"
                    "True if available, False if unavailable."
    )

class UpdateBook(NewBook):
    """
   Model for updating existing book information.
   Inherits validators and the `title` and `author` fields from `NewBook`
   """
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Children of Blood and Bone",
                "author": "Tomi Adeyemi"
            }
        }}
#
# class BookQueryParams(BaseModel):
#     author: Optional[str] = Field(None)
#     available: Optional[bool] = Field(None)
#     search: Optional[str] = Field(None)
#     skip: int = Field(0, ge=0)
#     limit: int = Field(10, ge=1, le=20)