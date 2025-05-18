from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from smart_solutions.app.core.deps import SessionDep, get_current_active_superuser
from smart_solutions.app.crud.user import insert_user, get_user_by_email
from smart_solutions.app.schemas.user import UserCreate, UserRead, UserPublic


router = APIRouter(prefix="/user", tags=["user"])

"""
Create a user and add it to database
Reuirements:
    - Check if the email entered is already in the database if the Email is already added
      return status code HTTP_400_BAD_REQUEST 
    - if the email does not exist in the database create the new user after validating against UserCreate Schema
"""
@router.post("/", 
             dependencies=[Depends(get_current_active_superuser)],
             response_model=UserRead)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    user = get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = insert_user(session=session, user_create=user_in)
    return user


@router.post("/signup", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = insert_user(session=session, user_create=user_create)
    return user


@router.get("/signup", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = insert_user(session=session, user_create=user_create)
    return user