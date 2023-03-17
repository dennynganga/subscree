from sqlalchemy.orm import Session

from src import auth
from src.data.users.db import UserDAO, UserAccountDAO
from src.data.users.models import UserCreate


def add_user(session: Session, user: UserCreate):
    new_user = session.query(UserDAO).filter(UserDAO.email == user.email).first()
    if not new_user:
        hashed_password = auth.hash_password(user.password)
        user_dict = user.dict()
        user_dict["password"] = hashed_password
        new_user = UserDAO(**user_dict)
        session.add(new_user)
        session.flush()
        session.refresh(new_user)
    return new_user


def add_user_to_account(session: Session, user_id: str, account_id: str):
    user_account = UserAccountDAO(user_id=user_id, account_id=account_id)
    session.add(user_account)
    session.flush()
    session.refresh(user_account)
    return


def retrieve_user_by_email(session: Session, user_email: str):
    return session.query(UserDAO).filter(UserDAO.email == user_email).first()


def retrieve_user_by_id(session: Session, user_id: str, account_id: str):
    user = session.query(UserDAO).filter(UserDAO.id == user_id).first()
    if not user:
        return
    # check if user can be accessed from this account
    if check_user_in_account(session=session, user_id=user.id, account_id=account_id):
        return user


def retrieve_account_users(session: Session, account_id: str):
    account_users = (
        session.query(UserDAO)
        .join(UserAccountDAO)
        .filter(UserAccountDAO.account_id == account_id)
    ).all()
    return account_users


def check_user_in_account(session: Session, user_id: str, account_id: str):
    return session.query(UserAccountDAO).filter(UserAccountDAO.user_id == user_id, UserAccountDAO.account_id == account_id).first()
