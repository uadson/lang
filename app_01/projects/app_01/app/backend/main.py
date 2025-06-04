from fastapi import FastAPI
from .routers.language import router as language_router

app = FastAPI()
app.include_router(language_router, prefix="/api/v1")
