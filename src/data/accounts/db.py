from sqlalchemy import String, Column, TIMESTAMP, func, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from src.data.base import Base


class AccountDAO(Base):

    __tablename__ = "accounts"

    id = Column(BigInteger(), primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

    # created_by = Column(BigInteger(), ForeignKey("users.id"))
    # owner_id = Column(BigInteger(), ForeignKey("users.id"))

    added_at = Column(TIMESTAMP(timezone=False), server_default=func.current_timestamp(), nullable=False)
    deleted_at = Column(TIMESTAMP())

    # users = relationship("UserDAO", back_populates="accounts")
