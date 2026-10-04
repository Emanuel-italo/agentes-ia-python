from fastapi import APIRouter, Depends, HTTPException

from agentes_ia.api.dependencies import get_chat_service, get_settings
from agentes_ia.api.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    MessageSchema,
)
from agentes_ia.core.settings import Settings
from agentes_ia.infrastructure.llm_client import LLMError
from agentes_ia.services.chat_service import ChatService

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        mode="llm" if settings.api_key else "echo",
        model=settings.model,
    )


@router.post("/chat", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    history = [m.to_domain() for m in payload.messages]
    try:
        reply = service.reply(history)
    except LLMError as exc:
        raise HTTPException(status_code=502, detail=f"Falha no provedor de IA: {exc}")
    return ChatResponse(message=MessageSchema.from_domain(reply))
