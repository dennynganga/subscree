from sqlalchemy import Column, BigInteger, ForeignKey, String, TIMESTAMP, func, SmallInteger

from src.data.base import Base


class ProductDAO(Base):
    __tablename__ = "products"

    id = Column(BigInteger(), primary_key=True, unique=True, autoincrement=True)
    account_id = Column(BigInteger(), ForeignKey("accounts.id"))
    name = Column(String(100))

    added_at = Column(TIMESTAMP, server_default=func.current_timestamp)
    deleted_at = Column(TIMESTAMP, nullable=True)


class PlanDAO(Base):

    __tablename__ = "plans"

    id = Column(BigInteger(), primary_key=True, unique=True, autoincrement=True)
    product_id = Column(BigInteger(), ForeignKey("products.id"))
    config = Column()
    cycle_days = Column(SmallInteger())
    position = Column(SmallInteger())
