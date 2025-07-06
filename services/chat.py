from sqlalchemy.orm import Session

from models import Conversation, Thread
from schemas import ConversationCreate, ThreadCreate

# --- Thread ---


def create_thread(db: Session, thread: ThreadCreate):
    db_thread = Thread(**thread.dict())
    db.add(db_thread)
    db.commit()
    db.refresh(db_thread)
    return db_thread


def get_threads_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(Thread)
        .filter(Thread.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_thread(db: Session, thread_id: int):
    return db.query(Thread).filter(Thread.id == thread_id).first()


def delete_thread(db: Session, thread_id: int):
    db_thread = get_thread(db, thread_id)
    if db_thread:
        # Also delete all associated conversations
        db.query(Conversation).filter(Conversation.thread_id == thread_id).delete()
        db.delete(db_thread)
        db.commit()
    return db_thread


# --- Conversation ---


def create_conversation(db: Session, conversation: ConversationCreate):
    db_conversation = Conversation(**conversation.dict())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def get_conversations_by_thread(
    db: Session, thread_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(Conversation)
        .filter(Conversation.thread_id == thread_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
