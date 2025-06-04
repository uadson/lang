from fastapi import APIRouter, status, HTTPException
from service_translater import translater
import models as model

router = APIRouter(prefix="/text-input", tags=["text-input"])


@router.post(
    "/", status_code=status.HTTP_202_ACCEPTED, response_model=model.ChatResponse
)
async def text_input(request: model.ChatRequest):
    text = request.text.strip()

    if not text:
        raise HTTPException(
            detail="Campo de texto não pode estar vazio.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
