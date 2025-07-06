from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import Conversation, ConversationCreate, Thread, ThreadCreate
from services import chat

router = APIRouter()

# --- Thread Routes ---


@router.post("/threads/", response_model=Thread)
def create_new_thread(thread: ThreadCreate, db: Session = Depends(get_db)):
    return chat.create_thread(db=db, thread=thread)


@router.get("/threads/user/{user_id}", response_model=List[Thread])
def read_user_threads(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    threads = chat.get_threads_by_user(
        db, user_id=user_id, skip=skip, limit=limit
    )
    return threads


@router.get("/threads/{thread_id}", response_model=Thread)
def read_thread(thread_id: int, db: Session = Depends(get_db)):
    db_thread = chat.get_thread(db, thread_id=thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return db_thread


@router.delete("/threads/{thread_id}", response_model=Thread)
def delete_thread(thread_id: int, db: Session = Depends(get_db)):
    db_thread = chat.delete_thread(db, thread_id=thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return db_thread


# --- Conversation Routes ---


@router.post("/conversations/", response_model=Conversation)
def create_new_conversation(
    conversation: ConversationCreate, db: Session = Depends(get_db)
):
    # Here you would add the logic to:
    # 1. Get the user's question from the conversation.
    # 2. (Optional) Rewrite the question for better search results.
    # 3. Query the vector database for relevant context.
    # 4. Combine the question and context and send to an LLM.
    # 5. Get the LLM's response.
    # 6. Save the user's question and the LLM's response as conversations.

    # For now, we'll just save the user's message.
    return chat.create_conversation(db=db, conversation=conversation)


@router.get("/conversations/{thread_id}", response_model=List[Conversation])
def read_thread_conversations(
    thread_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    conversations = chat.get_conversations_by_thread(
        db, thread_id=thread_id, skip=skip, limit=limit
    )
    return conversations
