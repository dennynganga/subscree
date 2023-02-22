from sqlalchemy import Column, String, BigInteger, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.data.base import Base


class CustomerDAO(Base):
    __tablename__ = "customers"

    id = Column(BigInteger(), autoincrement=True, unique=True, primary_key=True, index=True)
    external_id = Column(String(60), index=True)
    email = Column(String(50))
    account = Column(BigInteger(), ForeignKey("accounts.id"))

    added_at = Column(TIMESTAMP, server_default=func.current_timestamp)
    deleted_at = Column(TIMESTAMP, nullable=True)

    accounts = relationship("Account", back_populates="customers")