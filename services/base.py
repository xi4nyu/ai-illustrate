from abc import ABC
from database import get_db
from services.query import QueryMixin


class BaseService(ABC, QueryMixin):
    """Base service class for all services"""

    _model = None  # Subclasses must specify the model

    def __init__(self):
        self.db = next(get_db())

