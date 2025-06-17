from sqlmodel import Session, create_engine, SQLModel
from backend.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)
