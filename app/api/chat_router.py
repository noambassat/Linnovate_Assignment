# app/api/chat_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.pgvector_client import get_similar_highlights

router = APIRouter(prefix="")  # חשוב! בלי /chat כפול

class ChatRequest(BaseModel):
    query: str
    top_k: int = 3

@router.post("/chat")
def chat_with_video_highlights(request: ChatRequest):
    try:
        results = get_similar_highlights(request.query, request.top_k)
        return {"matches": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
