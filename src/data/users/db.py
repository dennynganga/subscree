from sqlalchemy import Column, String, BigInteger, TIMESTAMP, func, ForeignKey, Boolean

from src.data.base import Base


class UserDAO(Base):
    __tablename__ = "users"

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone_number = Column(String(30))
    password = Column(String(100))

    added_at = Column(TIMESTAMP(), server_default=func.current_timestamp(), nullable=False)
    deleted_at = Column(TIMESTAMP(), nullable=True)


class UserAccountDAO(Base):
    __tablename__ = "user_accounts"

    user_id = Column(
        BigInteger(), ForeignKey("users.id"), primary_key=True, nullable=False
    )
    account_id = Column(
        BigInteger(), ForeignKey("accounts.id"), primary_key=True, nullable=False
    )
