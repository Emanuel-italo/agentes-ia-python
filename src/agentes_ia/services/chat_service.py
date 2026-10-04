from agentes_ia.domain.models import Message, Role
from agentes_ia.infrastructure.llm_client import LLMClient


class ChatService:
    def __init__(self, client: LLMClient, system_prompt: str | None = None) -> None:
        self._client = client
        self._system_prompt = system_prompt

    def reply(self, history: list[Message]) -> Message:
        messages = list(history)
        if self._system_prompt and not any(m.role is Role.SYSTEM for m in messages):
            messages.insert(0, Message(Role.SYSTEM, self._system_prompt))
        content = self._client.complete(messages)
        return Message(Role.ASSISTANT, content)
