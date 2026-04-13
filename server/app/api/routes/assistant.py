from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import DEFAULT_BACKBOARD_ASSISTANT_ID
from app.services.assistant_service import (
    create_thread_for_assistant,
    send_message_to_thread,
)

router = APIRouter(prefix="/assistant", tags=["assistant"])


class CreateThreadRequest(BaseModel):
    assistant_id: Optional[str] = None


class SendMessageRequest(BaseModel):
    thread_id: str
    content: str
    web_search: Optional[str] = None
    memory: Optional[str] = None


@router.post("/threads")
async def create_thread(request: CreateThreadRequest):
    assistant_id = request.assistant_id or DEFAULT_BACKBOARD_ASSISTANT_ID

    if not assistant_id:
        raise HTTPException(
            status_code=400,
            detail="assistant_id is required or set DEFAULT_BACKBOARD_ASSISTANT_ID in .env",
        )

    try:
        thread = await create_thread_for_assistant(assistant_id)
        return {
            "thread_id": thread.thread_id,
            "assistant_id": assistant_id,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/messages")
async def send_message(request: SendMessageRequest):
    try:
        response_text = await send_message_to_thread(
            thread_id=request.thread_id,
            content=request.content,
            web_search=request.web_search,
            memory=request.memory,
            stream=True,
        )
        return {
            "thread_id": request.thread_id,
            "content": response_text,
            "web_search": request.web_search,
            "memory": request.memory,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc