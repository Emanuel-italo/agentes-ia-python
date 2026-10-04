import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str
    model: str
    timeout: float
    cors_origins: list[str]


def load_settings() -> Settings:
    origins = os.getenv("CORS_ORIGINS", "*")
    return Settings(
        api_key=os.getenv("LLM_API_KEY", ""),
        base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        timeout=float(os.getenv("LLM_TIMEOUT", "60")),
        cors_origins=[o.strip() for o in origins.split(",") if o.strip()],
    )
