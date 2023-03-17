from sqlalchemy import Column, BigInteger, ForeignKey, Date, TIMESTAMP, func, String

from src.data.base import Base
from src.data.utils import generate_unique_key


class SubscriptionDAO(Base):
    __tablename__ = "subscriptions"

    id = Column(String(30), primary_key=True, default=generate_unique_key, index=True)
    customer_id = Column(BigInteger(), ForeignKey("customers.id"))
    plan_id = Column(BigInteger(), ForeignKey("plans.id"))

    added_at = Column(TIMESTAMP, server_default=func.current_timestamp)
    next_renewal_date = Column(Date)
    deleted_at = Column(TIMESTAMP, nullable=True)
