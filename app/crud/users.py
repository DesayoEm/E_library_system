from uuid import uuid4
from fastapi import HTTPException
from typing import Optional, Dict
from schemas.user_schemas import User, NewUser, UpdateUser
from data.users import users
from exceptions import EmailLinkedError, EmailRegisteredError
from services.user_services import UserService


class UserCrud:
    def __init__(self, data: Dict[str, User], user_service: UserService):
        self.user_service = user_service
        self.users = data

    def create_user(self, new_user: NewUser) -> Dict:
        try:
            self.user_service.check_duplicate_user(new_user)
        except EmailLinkedError as e:
            raise HTTPException(status_code=409, detail=str(e))

        user_id = str(uuid4())
        created_user = User(id=user_id, is_active=True, **new_user.model_dump())
        self.users[user_id] = created_user

        return created_user.model_dump(exclude=["id"])


    def get_all_users(self) -> Dict[str, User]:
        if not self.users:
            raise HTTPException(status_code=404, detail="No users found")
        return self.users


    def get_user(self, user_id: str) -> User:
        if user_id not in self.users:
            raise HTTPException(status_code=404, detail="User not found")
        return self.users[user_id]


    def update_user(self, user_id: str, data: UpdateUser) -> User:
        user = self.get_user(user_id)
        try:
            self.user_service.check_duplicate_user_during_update(user_id, data)
        except EmailRegisteredError as e:
            raise HTTPException(status_code=409, detail=str(e))

        for field in ["name", "email"]:
            setattr(user, field, getattr(data, field))

        self.users[user_id] = user
        return user


    def deactivate_user(self, user_id: str) -> User:
        user= self.get_user(user_id)
        user.is_active= False
        self.users[user_id] = user
        return user


    def delete_user(self, user_id: str) -> None:
        user= self.get_user(user_id)
        del users[user_id]


user_crud = UserCrud(users, UserService())