import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.user import User
from services.user import UserService

from settings import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])



def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """获取当前用户"""
    token = credentials.credentials
    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = UserService.get_user(token_data["sub"])
    return user
