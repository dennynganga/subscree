import datetime

from sqlalchemy.orm import Session

from src.data.accounts.db import AccountDAO
from src.data.accounts.models import AccountCreate


def create_account(session: Session, account: AccountCreate):
    acc = session.query(AccountDAO).filter(AccountDAO.name == account.name).first()
    if not acc:
        acc = AccountDAO(name=account.name)
        session.add(acc)
        session.flush()
        session.refresh(acc)
    return acc


def fetch_accounts(session: Session, offset: int = 0, limit: int = 50):
    return session.query(AccountDAO).offset(offset).limit(limit).all()


def fetch_account(session: Session, account_id: int):
    return session.query(AccountDAO).filter(AccountDAO.id == account_id).first()


def delete_account(session: Session, account_id):
    account = fetch_account(session, account_id)
    account.deleted_at = datetime.datetime.utcnow()
    session.flush()
    return
