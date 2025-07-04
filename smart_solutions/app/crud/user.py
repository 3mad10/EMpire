import uuid
from typing import Any
from sqlmodel import Session
from sqlalchemy import text
from smart_solutions.app.models.user import User
from smart_solutions.app.core.security import (
    get_password_hash,
    verify_password
)
from smart_solutions.app.schemas.user import (
    UserCreate,
    UserRead
    )


def insert_user(*, session: Session, 
                user_create: User) -> UserCreate:
    db_obj = User.model_validate(
        user_create,
        update={"password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_by_email(*, session: Session, 
                      email: str) -> UserRead | None:
    query = text("SELECT * FROM user WHERE email = :user_email")
    session_user = session.execute(query, {"user_email": email}).first()
    return session_user


def authenticate(*, session: Session, 
                 email: str, password: str) -> UserRead | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
