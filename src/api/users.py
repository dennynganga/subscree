from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

from src.auth import get_current_user, authenticate_user, create_access_token
from src.data.base import session_scope
from src.data.users import crud as users_crud
from src.data.users.crud import add_user_to_account
from src.data.users.models import User, UserCreate

router = APIRouter()


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(session_scope)):
    error_msg = "Incorrect email or password."
    user = authenticate_user(email=form_data.username, password=form_data.password, session=session)
    if not user:
        raise HTTPException(status_code=400, detail=error_msg, headers={"WWW-Authenticate": "Bearer"})
    token_data = {"sub": user.email}
    access_token = create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/users", response_model=User)
def add_user(user: UserCreate, request: Request, session: Session = Depends(session_scope)):
    account_id = request.state.account_id
    user = users_crud.add_user(session=session, user=user)
    add_user_to_account(session=session, account_id=account_id, user_id=user.id)
    return user


@router.get("/users", response_model=list[User])
def get_users(request: Request, session: Session = Depends(session_scope)):
    account_id = request.state.account_id
    return users_crud.retrieve_account_users(session=session, account_id=account_id)


@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: str, request: Request, session: Session = Depends(session_scope)):
    account_id = request.state.account_id
    user = users_crud.retrieve_user_by_id(session=session, user_id=user_id, account_id=account_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


