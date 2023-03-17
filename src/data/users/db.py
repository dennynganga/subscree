from sqlalchemy import Column, String, BigInteger, TIMESTAMP, func, ForeignKey, Boolean

from src.data.base import Base
from src.data.utils import generate_unique_key


class UserDAO(Base):
    __tablename__ = "users"

    id = Column(String(30), primary_key=True, default=generate_unique_key, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone_number = Column(String(30))
    password = Column(String(100), nullable=False)

    added_at = Column(TIMESTAMP(), server_default=func.current_timestamp(), nullable=False)
    disabled_at = Column(TIMESTAMP(), nullable=True)


class UserAccountDAO(Base):
    __tablename__ = "user_accounts"

    user_id = Column(
        String(30), ForeignKey("users.id"), primary_key=True, nullable=False
    )
    account_id = Column(
        String(30), ForeignKey("accounts.id"), primary_key=True, nullable=False
    )
