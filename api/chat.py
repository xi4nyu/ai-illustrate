from fastapi import APIRouter, Depends, HTTPException

from utils.jwt import get_current_user
from schemas import ConversationCreate, ThreadCreate, R
from services.chat import ThreadService, ConversationService
from schemas.user import User

router = APIRouter()

# --- Thread Routes ---


@router.post("/threads/")
def create_new_thread(
    thread: ThreadCreate, current_user: User = Depends(get_current_user)
):
    thread.user_id = current_user.id
    ret = ThreadService.create_thread(thread=thread)
    return R(data=ret)


@router.get("/threads/user/")
def read_user_threads(
    page: int = 1, limit: int = 20, current_user: User = Depends(get_current_user)
):
    threads = ThreadService.get_threads_by_user(
        user_id=current_user.id, page=page, limit=limit
    )
    return R(data=threads)


@router.get("/threads/{thread_id}")
def read_thread(thread_id: int, current_user: User = Depends(get_current_user)):
    db_thread = ThreadService.get_thread(thread_id=thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return R(data=db_thread)


@router.delete("/threads/{thread_id}")
def delete_thread(thread_id: int, current_user: User = Depends(get_current_user)):
    db_thread = ThreadService.delete_thread(thread_id=thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return R(data=db_thread)


# --- Conversation Routes ---


@router.post("/conversations/")
def create_new_conversation(
    conversation: ConversationCreate,
    current_user: User = Depends(get_current_user),
):
    # Here you would add the logic to:
    # 1. Get the user's question from the conversation.
    # 2. (Optional) Rewrite the question for better search results.
    # 3. Query the vector database for relevant context.
    # 4. Combine the question and context and send to an LLM.
    # 5. Get the LLM's response.
    # 6. Save the user's question and the LLM's response as conversations.

    # For now, we'll just save the user's message.
    conversation.user_id = current_user.id
    ret = ConversationService.create_conversation(conversation=conversation)
    return R(data=ret)


@router.get("/conversations/{thread_id}")
def read_thread_conversations(
    thread_id: int,
    page: int = 1,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
):
    conversations = ConversationService.get_conversations_by_thread(
        thread_id=thread_id, user_id=current_user.id, page=page, limit=limit
    )
    return R(data=conversations)
