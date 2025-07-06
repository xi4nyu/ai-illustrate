from typing import Any
from fastapi import status
from pydantic import BaseModel


class Response(BaseModel):
    code: int = status.HTTP_200_OK
    message: str = ""
    data: Any = None


R = Response
