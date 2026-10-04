from pydantic import BaseModel, Field

from agentes_ia.domain.models import Message, Role


class MessageSchema(BaseModel):
    role: Role
    content: str = Field(min_length=1)

    def to_domain(self) -> Message:
        return Message(role=self.role, content=self.content)

    @classmethod
    def from_domain(cls, message: Message) -> "MessageSchema":
        return cls(role=message.role, content=message.content)


class ChatRequest(BaseModel):
    messages: list[MessageSchema] = Field(min_length=1)


class ChatResponse(BaseModel):
    message: MessageSchema


class HealthResponse(BaseModel):
    status: str
    mode: str
    model: str
