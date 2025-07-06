from typing import List

from fastapi import APIRouter, HTTPException

from schemas.user import User, UserCreate, UserLogin, UserUpdate
from services.user import UserService
from utils.jwt import create_access_token
from utils.secure import verify_password

router = APIRouter()


@router.post("/", response_model=User)
def register(user: UserCreate):
    db_user = UserService.get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return UserService.create_user(user=user)


@router.post("/login", response_model=User)
def login(user: UserLogin):
    db_user = UserService.get_user_by_username(username=user.username)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": db_user.id})
    ret = {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user
    }
    return ret


@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100):
    users = UserService.get_users(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int):
    db_user = UserService.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate):
    db_user = UserService.update_user(user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int):
    db_user = UserService.delete_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
