from sqlalchemy import String, Column, TIMESTAMP, func, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from src.data.base import Base
from src.data.utils import generate_unique_key


class AccountDAO(Base):

    __tablename__ = "accounts"

    id = Column(String(30), primary_key=True, default=generate_unique_key, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    country = Column(String(5), nullable=False)

    # created_by = Column(String(30), ForeignKey("users.id"))
    owner_id = Column(String(30), ForeignKey("users.id"))

    added_at = Column(TIMESTAMP(timezone=False), server_default=func.current_timestamp(), nullable=False)
    deleted_at = Column(TIMESTAMP())

    # users = relationship("UserDAO", back_populates="accounts")
