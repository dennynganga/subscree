from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from src.auth import oauth2_scheme
from src.data.accounts import crud
from src.data.accounts.models import Account, AccountCreate
from src.data.base import session_scope

router = APIRouter()


@router.get("/accounts/", response_model=list[Account])
def get_accounts(token: str = Depends(oauth2_scheme), session: Session = Depends(session_scope)):
    print(token)
    return crud.fetch_accounts(session=session, offset=0, limit=50)


@router.post("/accounts/", response_model=Account)
def create_account(account: AccountCreate, session: Session = Depends(session_scope)):
    return crud.create_account(session=session, account=account)


@router.get("/accounts/{account_id}", response_model=Account)
def get_account(account_id: int, session: Session = Depends(session_scope)):
    account = crud.fetch_account(session=session, account_id=account_id)
    if not account:
        msg: str = f"Invalid account ID: {account_id}"
        raise HTTPException(status_code=404, detail=msg)
    return account
