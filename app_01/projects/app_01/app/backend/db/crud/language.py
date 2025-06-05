from backend.models import language as model
from sqlmodel import Session, select
import uuid


def create_language(db: Session, language: model.LanguageCreate) -> model.Language:
    db_language = model.Language.model_validate(language)
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language


def list_languages(db: Session) -> list[model.Language]:
    result = db.exec(select(model.Language))
    return result.all()


def get_language(db: Session, language_id: uuid.UUID) -> model.Language:
    result = db.exec(select(model.Language).where(model.Language.id == language_id))
    language = result.one_or_none()
    return language
