from sqlalchemy import Column, String, BigInteger, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.data.base import Base
from src.data.utils import generate_unique_key


class CustomerDAO(Base):
    __tablename__ = "customers"

    id = Column(String(30), primary_key=True, default=generate_unique_key, index=True)
    external_id = Column(String(60), index=True)
    email = Column(String(50), nullable=False)
    account_id = Column(String(30), ForeignKey("accounts.id"))

    added_at = Column(TIMESTAMP(), server_default=func.current_timestamp())
    deleted_at = Column(TIMESTAMP(), nullable=True)

    # accounts = relationship("Account", back_populates="customers")
