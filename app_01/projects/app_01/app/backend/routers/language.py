from backend.models import language as model
from backend.db.crud import language as crud
from backend.db.database import get_session
from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session
import uuid

router = APIRouter(prefix="/languages", tags=["Languages"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=model.LanguageResponse
)
def create(language: model.LanguageCreate, db: Session = Depends(get_session)):
    try:
        return crud.create_language(db, language)
    except Exception as e:
        raise HTTPException(
            detail=f"Erro ao tentar registrar idioma: {e}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[model.LanguageResponse]
)
def list_all(db: Session = Depends(get_session)):
    return crud.list_languages(db)


@router.get(
    "/language_id",
    status_code=status.HTTP_200_OK,
    response_model=model.LanguageResponse,
)
def get_one(db: Session = Depends(get_session), language_id: uuid.UUID = None):
    language = crud.get_language(db, language_id)
    if not language:
        raise HTTPException(
            detail="Idioma não encontrado", status_code=status.HTTP_404_NOT_FOUND
        )
    return language
