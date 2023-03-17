import datetime

from sqlalchemy.orm import Session

from src.data.accounts.db import AccountDAO
from src.data.accounts.models import AccountCreate


def create_account(session: Session, account: AccountCreate, owner_id: str):
    acc = AccountDAO(name=account.name, country=account.country, owner_id=owner_id)
    session.add(acc)
    session.flush()
    session.refresh(acc)
    return acc


def fetch_accounts(session: Session, offset: int = 0, limit: int = 50):
    return session.query(AccountDAO).offset(offset).limit(limit).all()


def retrieve_account_by_id(session: Session, account_id: str):
    return session.query(AccountDAO).filter(AccountDAO.id == account_id).first()


def retrieve_account_by_name(session: Session, account_name: str):
    return session.query(AccountDAO).filter(AccountDAO.name == account_name).first()


def delete_account(session: Session, account_id):
    account = retrieve_account_by_id(session, account_id)
    account.deleted_at = datetime.datetime.utcnow()
    session.flush()
    return
