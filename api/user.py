from typing import List

from fastapi import APIRouter, Depends, HTTPException

from schemas.user import User, UserCreate, UserLogin, UserUpdate
from schemas.api import R
from services.user import UserService
from utils.jwt import create_access_token, get_current_user
from utils.secure import verify_password

router = APIRouter()


@router.post("/register")
def register(user: UserCreate):
    db_user = UserService.get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user.role = ""
    ret = UserService.create_user(user=user)
    return R(data=ret)


@router.post("/login")
def login(user: UserLogin):
    db_user = UserService.get_user_by_username(username=user.username)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": f"{db_user.id}"})
    ret = {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"username": db_user.username, "role": db_user.role},
    }
    return R(data=ret)


@router.get("/")
def read_users(page: int = 1, limit: int = 20, _: User = Depends(get_current_user)):
    users = UserService.get_users(page=page, limit=limit)
    return R(data=[User.from_orm(user) for user in users])


@router.get("/{user_id}")
def read_user(user_id: int, _: User = Depends(get_current_user)):
    db_user = UserService.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return R(data=User.from_orm(db_user))


@router.put("/{user_id}")
def update_user(
    user_id: int, user: UserUpdate, current_user: User = Depends(get_current_user)
):
    user.updated_uid = current_user.id
    UserService.update_user(user_id=user_id, user_update=user)

    return R(data={"user_id": user_id})


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    UserService.delete_user(user_id=user_id)
    return R(data={"user_id": user_id})
