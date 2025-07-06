from models import Conversation, Thread
from schemas import ConversationCreate, ThreadCreate
from services.base import BaseService


class ThreadService(BaseService):
    _model = Thread

    @classmethod
    def create_thread(cls, thread: ThreadCreate):
        return cls.insert(thread.dict())

    @classmethod
    def get_threads_by_user(cls, user_id: int, page: int = 1, limit: int = 100):
        return cls.get_list(page=page, limit=limit, joined_user=False, user_id=user_id)

    @classmethod
    def get_thread(cls, thread_id: int):
        return cls.get_one(id=thread_id)

    @classmethod
    def delete_thread(cls, thread_id: int):
        db_thread = cls.get_thread(thread_id)
        if db_thread:
            # Also delete all associated conversations
            cls.db.query(Conversation).filter(
                Conversation.thread_id == thread_id
            ).delete(synchronize_session=False)
            cls.db.delete(db_thread)
            cls.db.commit()
        return db_thread


class ConversationService(BaseService):
    _model = Conversation

    @classmethod
    def create_conversation(cls, conversation: ConversationCreate):
        return cls.insert(conversation.dict())

    @classmethod
    def get_conversations_by_thread(
        cls, thread_id: int, user_id: int, page: int = 1, limit: int = 20
    ):
        return cls.get_list(
            page=page,
            limit=limit,
            joined_user=False,
            thread_id=thread_id,
            user_id=user_id,
        )
