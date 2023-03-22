from sqlalchemy import Column, BigInteger, ForeignKey, Date, TIMESTAMP, func, String, Boolean

from src.data.base import Base
from src.data.utils import generate_unique_key


class CycleCounterDAO(Base):
    __tablename__ = "cycle_counter"

    id = Column(String(30), primary_key=True, default=generate_unique_key, index=True)
    customer_id = Column(String(30), ForeignKey("customers.id"))
    ext_id = Column(String(30), ForeignKey("products_ext.id"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    count = Column(BigInteger(), default=0)
    complete = Column(Boolean(), default=False)


class SubscriptionDAO(Base):
    __tablename__ = "subscriptions"

    id = Column(String(30), primary_key=True, default=generate_unique_key, index=True)
    customer_id = Column(BigInteger(), ForeignKey("customers.id"))
    plan_id = Column(BigInteger(), ForeignKey("plans.id"))

    added_at = Column(TIMESTAMP, server_default=func.current_timestamp)
    next_charge_date = Column(Date)
    deleted_at = Column(TIMESTAMP, nullable=True)
