from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os

from app.core.rag import Retriever
from app.core.llm_client import LLMClient
from app.models.schemas import ChatMessage, ChatResponse

router = APIRouter()

# singletons / factories could be improved for DI
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini")
DOCS_PATH = os.environ.get("DOCS_PATH", "./src/app/data")

retriever = Retriever(docs_path=DOCS_PATH, embedding_model=EMBEDDING_MODEL)
llm_client = LLMClient(model=LLM_MODEL)


class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: Optional[str] = None


@router.post("/message", response_model=ChatResponse)
async def process_message(req: ChatRequest, request: Request):
    """
    Main entry point for user messages.
    - Uses Retriever to fetch context
    - Uses LLM to generate final answer
    - Stores message in Redis conversational memory (app.state.memory)
    """
    memory = request.app.state.memory
    # fetch relevant docs
    contexts = await retriever.get_relevant_chunks(req.message, top_k=4)

    # include short conversation history from Redis
    convo_key = f"convo:{req.conversation_id or req.user_id}"
    history = await memory.get_messages(convo_key, limit=6)

    prompt = llm_client.build_prompt(user_message=req.message, history=history, contexts=contexts)
    response_text = await llm_client.generate(prompt)

    # persist message + assistant response to memory
    await memory.append_message(convo_key, {"role": "user", "text": req.message})
    await memory.append_message(convo_key, {"role": "assistant", "text": response_text})

    return ChatResponse(
        reply=response_text,
        used_contexts=[c.meta for c in contexts],
    )
