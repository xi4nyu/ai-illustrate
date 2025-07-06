from models import Conversation, Thread
from schemas import ConversationCreate, ThreadCreate
from services.base import BaseService


class ThreadService(BaseService):
    _model = Thread

    def create_thread(self, thread: ThreadCreate):
        return self.insert(thread.dict())

    def get_threads_by_user(self, user_id: int, skip: int = 0, limit: int = 100):
        page = skip // limit + 1
        return self.get_list(page=page, limit=limit, joined_user=False, user_id=user_id)

    def get_thread(self, thread_id: int):
        return self.get_one(id=thread_id)

    def delete_thread(self, thread_id: int):
        db_thread = self.get_thread(thread_id)
        if db_thread:
            # Also delete all associated conversations
            self.db.query(Conversation).filter(
                Conversation.thread_id == thread_id
            ).delete(synchronize_session=False)
            self.db.delete(db_thread)
            self.db.commit()
        return db_thread


class ConversationService(BaseService):
    _model = Conversation

    def create_conversation(self, conversation: ConversationCreate):
        return self.insert(conversation.dict())

    def get_conversations_by_thread(
        self, thread_id: int, skip: int = 0, limit: int = 100
    ):
        page = skip // limit + 1
        return self.get_list(
            page=page, limit=limit, joined_user=False, thread_id=thread_id
        )
