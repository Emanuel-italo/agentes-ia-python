from functools import lru_cache

from agentes_ia.core.settings import Settings, load_settings
from agentes_ia.infrastructure.llm_client import build_client
from agentes_ia.services.chat_service import ChatService


@lru_cache
def get_settings() -> Settings:
    return load_settings()


@lru_cache
def get_chat_service() -> ChatService:
    return ChatService(
        build_client(get_settings()),
        system_prompt="Você é um assistente prestativo.",
    )
