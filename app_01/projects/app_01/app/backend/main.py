from fastapi import FastAPI
from .routers.language import router as language_router
from .routers.translate import router as translate_router
from .db.database import init_db

PREFIX = "/api/v1"

app = FastAPI()
app.include_router(language_router, prefix=PREFIX)
app.include_router(translate_router, prefix=PREFIX)


@app.on_event("startup")
async def startup():
    init_db()
