from sqlmodel import Session, create_engine, SQLModel
from smart_solutions.app.core.config import settings
from typing import Annotated
from fastapi import Depends
from smart_solutions.app.schemas.user import UserRead
from fastapi import HTTPException

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)


def create_db_and_tables() -> None:
    # print(f"Create DB On : {settings.SQLALCHEMY_DATABASE_URI}")
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_current_active_superuser(current_user) -> UserRead:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
