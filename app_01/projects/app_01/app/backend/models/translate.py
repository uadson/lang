from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class TranslateRequestBase(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    text: str
    source_language_id: uuid.UUID
    target_language_id: uuid.UUID


class TranslateRequest(TranslateRequestBase):
    request_id: uuid.UUID | None = Field(default_factory=uuid.uuid4)


class TranslateResponseBase(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    translated_text: str


class TranslateResponse(TranslateResponseBase):
    response_id: uuid.UUID | None = Field(default_factory=uuid.uuid4)
    source_language: str
    target_language: str
