from models.user import User
from schemas.user import UserCreate, UserUpdate
from services.base import BaseService
from utils.secure import get_password_hash


class UserService(BaseService):
    _model = User

    def get_user(self, user_id: int):
        return self.get_one(id=user_id)

    def get_user_by_username(self, username: str):
        return self.get_one(username=username)

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.get_list(skip=skip, limit=limit)

    def create_user(self, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        
        user_data = {
            "username": user.username,
            "password": hashed_password,
            "role": user.role
        }
        db_user = self.insert(user_data)
        return db_user

    def update_user(self, user_id: int, user_update: UserUpdate):
        return self.update(user_id, user_update)

    def delete_user(self, user_id: int):
        return self.delete(id=user_id)
