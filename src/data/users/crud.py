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


def retrieve_user_by_email(session: Session, user_email: str):
    return session.query(UserDAO).filter(UserDAO.email == user_email).first()


def retrieve_user_by_id(session: Session, user_id: int):
    return session.query(UserDAO).filter(UserDAO.id == user_id).first()


def retrieve_account_users(session: Session, account_id: int):
    account_users = (
        session.query(UserDAO)
        .join(UserAccountDAO)
        .filter(UserAccountDAO.account_id == account_id)
    ).all()
    return account_users
