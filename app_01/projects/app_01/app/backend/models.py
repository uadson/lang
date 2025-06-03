from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class ChatRequestBase(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    text: str


class ChatRequest(ChatRequestBase):
    request_id: uuid.UUID | None = Field(default_factory=uuid.uuid4)


class ChatResponseBase(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    response: str


class ChatResponse(ChatResponseBase):
    response_id: uuid.UUID | None = Field(default_factory=uuid.uuid4)
