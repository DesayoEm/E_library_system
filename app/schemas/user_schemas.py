from pydantic import BaseModel, EmailStr, field_validator, Field

class NewUser(BaseModel):
    """Base model for creating a new user."""
    name: str = Field (
        description="The user's full name",
        examples=["Ade Love"],
        min_length=2

    )
    email: EmailStr = Field(
        description="The user's email address",
        examples=["ade@gmail.com"]
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Ade Love",
                "email": "ade@gmail.com"
            }
        }}


class User(NewUser):
    """Complete user model with system generated fields: `id` and `status`."""
    id: str
    is_active: bool = True


class UpdateUser(NewUser):
    """model for updating a new user."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Festus Dairo",
                "email": "festusd@gmail.com"
            }
        }}

