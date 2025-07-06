from sqlalchemy import desc
from database import get_db


db = next(get_db())


class QueryMixin:
    """通用查询辅助类，提供简单的查询接口"""

    _model = None  # 子类必须指定

    OPERATORS = {
        "exact": lambda field, value: field == value,
        "gte": lambda field, value: field >= value,
        "lte": lambda field, value: field <= value,
        "gt": lambda field, value: field > value,
        "lt": lambda field, value: field < value,
        "in": lambda field, value: field.in_(value),
        "is_null": lambda field, value: field.is_(None),
        "contains": lambda field, value: field.contains(value)
    }

    @classmethod
    def _parse_filter(cls, key: str, value: str) -> tuple[str, str, str]:
        """解析 key，例如 id__gte => (字段, 操作符)"""
        if "__" in key:
            field_name, op = key.split("__", 1)
        else:
            field_name, op = key, "exact"
        return field_name, op, value

    @classmethod
    def _parse_filters(cls, filters, query):
        for key, value in filters.items():
            field_name, op, value = cls._parse_filter(key, value)
            field = getattr(cls._model, field_name)
            query = query.filter(cls.OPERATORS[op](field, value))
        return query

    @classmethod
    def get_one(cls, **filters: None | dict) -> object | None:
        """获取一条记录"""
        query = cls._parse_filters(filters, cls._model.query)
        return query.first()

    @classmethod
    def get_list(
        cls, page: int = 1, limit: int = 20, joined_user=True, **filters: None | dict
    ) -> list[object]:
        """获取记录列表，支持分页"""
        offset = (page - 1) * limit
        query = cls._parse_filters(filters, cls._model.query)
        if joined_user:
            query = query.options(db.joinedload(cls._model.user))

        return query.order_by(desc("id")).limit(limit).offset(offset).all()

    @classmethod
    def get_all(cls, joined_user=False, **filters: None | dict) -> list[object]:
        """获取记录列表"""
        query = cls._parse_filters(filters, cls._model.query)
        if joined_user:
            query = query.options(db.joinedload(cls._model.user))

        return query.order_by(desc("id")).all()

    @classmethod
    def count(cls, **filters: None | dict) -> int:
        """统计符合条件的记录数"""
        query = cls._parse_filters(filters, cls._model.query)
        return query.count()

    @classmethod
    def delete(cls, **filters: None | dict) -> int:
        """删除符合条件的记录"""
        query = cls._parse_filters(filters, cls._model.query)
        deleted_count = query.delete(synchronize_session=False)
        db.session.commit()
        return deleted_count

    @classmethod
    def update(cls, update_values: dict, **filters: None | dict) -> object:
        """批量更新符合条件的记录"""
        # TODO: 优化这里更新方式
        query = cls._parse_filters(filters, cls._model.query)
        for field_name, value in update_values.items():
            field = getattr(cls._model, field_name)
            query = query.update({field: value}, synchronize_session=False)

        db.session.commit()
        return query

    @classmethod
    def insert(cls, data: dict | list) -> object | list:
        """
        插入记录。
        - data 可以是 dict 或 dict 列表。
        - 返回新增对象或对象列表。
        """
        if isinstance(data, dict):
            # 单条记录
            obj = cls._model(**data)
            db.session.add(obj)
            db.session.commit()
            return obj
        elif isinstance(data, list) and all(isinstance(d, dict) for d in data):
            # 批量新增
            objs = [cls._model(**d) for d in data]
            db.session.bulk_save_objects(objs)
            db.session.commit()
            return objs
        else:
            raise ValueError("数据格式错误，必须是 dict 或 dict 列表。")
