from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Any
from smart_solutions.app.api.deps import SessionDep, get_current_active_superuser
from smart_solutions.app.crud.user import insert_user, get_user_by_email, get_user_by_id
from smart_solutions.app.schemas.user import (
    UserCreate,
    UserRead,
    UserPublic,
    UserUpdate
)
from smart_solutions.app.api.deps import CurrentUser
from typing import Annotated
from uuid import UUID
from sqlmodel import select

router = APIRouter(prefix="/user", tags=["user"])

"""
Create a user and add it to database
Reuirements:
    - Check if the email entered is already in the database if the Email is already added
      return status code HTTP_400_BAD_REQUEST 
    - Check if the email address is a valid email by checking its regex and the mailing address (e.g. @gmail.com)
    - check if the phone number is a valid phone number iff the phone number is is passed as input 
      if the phone number is not valid return status code HTTP_400_BAD_REQUEST
    - Check that the country is a valid country iff a country is passed as input if it is invalid
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


@router.post("/signup",
             response_model=UserPublic)
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

@router.patch(
    "/me",
    response_model=UserPublic,
)
def update_user_me(
    *, session: SessionDep, user_in: UserUpdate, current_user: CurrentUser

) -> Any:
    """
    Update own user.
    """
    if user_in.email:
        existing_user = get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.get("/info/{user_id}",
             response_model=UserPublic)
def get_user_info_public(session: SessionDep, user_id: Annotated[UUID, Path(title="ID of the user")]) -> Any:
    user = get_user_by_id(session=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User with this ID does not exist",
        )
    return UserPublic.model_validate(user, from_attributes=True)