from fastapi import APIRouter, status, HTTPException, Depends
from backend.service_translater import translater
import backend.models.translate as model
import backend.models.language as model_language
from backend.db.database import get_session
from sqlmodel import Session, select

router = APIRouter(prefix="/translate", tags=["translate"])


@router.post(
    "/", status_code=status.HTTP_202_ACCEPTED, response_model=model.TranslateResponse
)
async def translate_text(
    request: model.TranslateRequest, db: Session = Depends(get_session)
):
    text = request.text.strip()

    source = db.exec(
        select(model_language.Language).where(
            model_language.Language.id == request.source_language_id
        )
    )
    source_language = source.one_or_none()

    target_language = db.exec(
        select(model_language.Language).where(
            model_language.Language.id == request.target_language_id
        )
    )

    target_language = target_language.one_or_none()

    if not text or not source_language.name or not target_language.name:
        raise HTTPException(
            detail="Campos de texto, idioma de origem e idioma de destino não podem estar vazios",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    translated_text = translater.translate(
        text, str(source_language.name), str(target_language.name)
    )

    return model.TranslateResponse(
        translated_text=translated_text,
        source_language=source_language.name,
        target_language=target_language.name,
    )
