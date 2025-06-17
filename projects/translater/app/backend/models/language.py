from datetime import datetime
from sqlmodel import Field, SQLModel
import uuid


class LanguageBase(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    name: str = Field(default=None, nullable=False, index=True, unique=True)


class Language(LanguageBase, table=True):
    __tablename__ = "languages"

    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)


class LanguageCreate(LanguageBase):
    pass


class LanguageResponse(SQLModel):
    id: uuid.UUID | None
    name: str | None
    created_at: datetime | None
