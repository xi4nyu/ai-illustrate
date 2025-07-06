from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from database import get_db
from utils.logger import logger


class DatabaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 为每个请求创建数据库会话
        with get_db() as db:
            # 将数据库会话存储在请求状态中
            request.state.db = db
            logger.info(f"Database session created for {request.url.path}")

            try:
                # 处理请求
                response = await call_next(request)
                logger.info(f"Request {request.url.path} completed successfully")
                return response
            except Exception as e:
                logger.error(f"Error in request {request.url.path}: {str(e)}")
                raise
            finally:
                # 数据库会话会在上下文管理器中自动关闭
                logger.info(f"Database session closed for {request.url.path}")


middleware = [
    DatabaseMiddleware,
]
