from models.user import User
from schemas.user import UserCreate, UserUpdate
from services.base import BaseService
from utils.secure import get_password_hash


class UserService(BaseService):
    _model = User

    @classmethod
    def get_user(cls, user_id: int):
        return cls.get_one(id=user_id)

    @classmethod
    def get_user_by_username(cls, username: str):
        return cls.get_one(username=username)

    @classmethod
    def get_users(cls, page: int = 1, limit: int = 20):
        return cls.get_list(page=page, limit=limit)

    @classmethod
    def create_user(cls, user: UserCreate):
        hashed_password = get_password_hash(user.password)

        user_data = {
            "username": user.username,
            "password": hashed_password,
            "role": user.role,
        }
        db_user = cls.insert(user_data)
        return db_user

    @classmethod
    def update_user(cls, user_id: int, user_update: UserUpdate):
        if user_update.password:
            user_update.password = get_password_hash(user_update.password)

        update_values = user_update.dict(exclude_unset=True)

        return cls.update(update_values, id=user_id)

    @classmethod
    def delete_user(cls, user_id: int):
        return cls.delete(id=user_id)
