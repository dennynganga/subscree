from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.auth import oauth2_scheme
from src.data.accounts import crud as accounts_crud
from src.data.users import crud as users_crud
from src.data.accounts.models import Account, AccountCreate
from src.data.base import session_scope
from src.data.users.crud import add_user_to_account

router = APIRouter()


@router.get("/accounts/", response_model=list[Account])
def get_accounts(token: str = Depends(oauth2_scheme), session: Session = Depends(session_scope)):
    return accounts_crud.fetch_accounts(session=session, offset=0, limit=50)


@router.post("/accounts/", response_model=Account)
def create_account(account: AccountCreate, session: Session = Depends(session_scope)):
    if accounts_crud.retrieve_account_by_name(session=session, account_name=account.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Account with name {account.name} already exists.")
    user = users_crud.add_user(session=session, user=account.owner)
    new_account = accounts_crud.create_account(session=session, account=account, owner_id=user.id)
    add_user_to_account(session=session, user_id=user.id, account_id=new_account.id)
    return new_account


@router.get("/accounts/{account_id}", response_model=Account)
def get_account(account_id: str, session: Session = Depends(session_scope)):
    account = accounts_crud.retrieve_account_by_id(session=session, account_id=account_id)
    if not account:
        msg: str = f"Invalid account ID: {account_id}"
        raise HTTPException(status_code=404, detail=msg)
    return account
