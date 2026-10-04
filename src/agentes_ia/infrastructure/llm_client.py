from typing import Protocol

import requests

from agentes_ia.core.settings import Settings
from agentes_ia.domain.models import Message


class LLMError(Exception):
    pass


class LLMClient(Protocol):
    def complete(self, messages: list[Message]) -> str: ...


class OpenAICompatibleClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def complete(self, messages: list[Message]) -> str:
        try:
            response = requests.post(
                f"{self._settings.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self._settings.api_key}"},
                json={
                    "model": self._settings.model,
                    "messages": [m.to_dict() for m in messages],
                },
                timeout=self._settings.timeout,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except (requests.RequestException, KeyError, IndexError, ValueError) as exc:
            raise LLMError(str(exc)) from exc


class EchoClient:
    def complete(self, messages: list[Message]) -> str:
        last = messages[-1].content if messages else ""
        return f"[modo eco, defina LLM_API_KEY] {last}"


def build_client(settings: Settings) -> LLMClient:
    if settings.api_key:
        return OpenAICompatibleClient(settings)
    return EchoClient()
