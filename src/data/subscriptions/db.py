from sqlalchemy import Column, BigInteger, ForeignKey, Date, TIMESTAMP, func

from src.data.base import Base


class SubscriptionDAO(Base):
    __tablename__ = "subscriptions"

    id = Column(BigInteger(), primary_key=True, index=True)
    customer_id = Column(BigInteger(), ForeignKey("customers.id"))
    plan_id = Column(BigInteger(), ForeignKey("plans.id"))

    added_at = Column(TIMESTAMP, server_default=func.current_timestamp)
    next_renewal_date = Column(Date)
    deleted_at = Column(TIMESTAMP, nullable=True)
