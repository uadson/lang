from backend.models import LanguageRequest, LanguageResponse
from datetime import datetime
import uuid


async def create_language(name: str) -> LanguageRequest:
    return LanguageRequest(id=uuid.uuid4(), name=name, created_at=datetime.now())


async def get_languages() -> list[LanguageRequest]:
    return list[LanguageResponse]()
