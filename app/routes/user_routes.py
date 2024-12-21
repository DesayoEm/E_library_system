from fastapi import APIRouter
from schemas.user_schemas import User, NewUser, UpdateUser
from crud.users import user_crud
from typing import Dict


user_router=APIRouter()

@user_router.post("/", status_code= 201)
def create_user(payload:NewUser) -> Dict :
    new_user = user_crud.create_user(payload)
    return new_user


@user_router.get("/" ,status_code= 200)
def get_all_users() -> Dict[str, User]:
    return user_crud.get_all_users()


@user_router.get("/{user_id}",status_code= 200)
def get_user(user_id: str) -> User:
    user=user_crud.get_user(user_id)
    return user


@user_router.put("/{user_id}" ,status_code= 200)
def update_user(user_id:str, data: UpdateUser) -> User:
    updated_user = user_crud.update_user(user_id, data)
    return updated_user


@user_router.patch("/{user_id}" ,status_code= 200)
def deactivate_user(user_id: str) -> User:
    deactivated_user = user_crud.deactivate_user(user_id)
    return deactivated_user


@user_router.delete("/{user_id}", status_code= 204)
def delete_user(user_id: str) -> None:
    user_crud.delete_user(user_id)


