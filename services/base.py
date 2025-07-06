from abc import ABC
from services.query import QueryMixin


class BaseService(ABC, QueryMixin):
    """Base service class for all services"""

    @classmethod
    def db(cls):
        return QueryMixin.db


