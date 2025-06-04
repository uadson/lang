from backend.models import LanguageRequest, LanguageResponse
from backend.db import crud
from fastapi import APIRouter, status, HTTPException

router = APIRouter(prefix="/languages", tags=["Languages"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=LanguageResponse)
async def create(request: LanguageRequest):
    language_name = request.name.strip()
    if not language_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome do idioma não pode ser vazio",
        )
    language = await crud.create_language(language_name)
    return language


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[LanguageResponse])
async def list_all():
    return await crud.get_languages()
