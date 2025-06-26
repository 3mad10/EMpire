import jwt
from sqlmodel import Session, create_engine, SQLModel
from smart_solutions.app.core.config import settings
from typing import Annotated
from fastapi import Depends
from smart_solutions.app.models.user import User, TokenPayload
from smart_solutions.app.core import security
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from fastapi import status

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


"""
Update to make the creation done by SqlAlchemy
"""
def create_db_and_tables() -> None:
    # print(f"Create DB On : {settings.SQLALCHEMY_DATABASE_URI}")
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
