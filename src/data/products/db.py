from enum import Enum

from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    TIMESTAMP,
    func,
    SmallInteger,
    Numeric,
    Enum as pg_enum,
    JSON,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from src.data.base import Base
from src.data.utils import generate_unique_key


class ProductBillingType(Enum):
    VOLUME = "volume"  # 1-1000 emails sent $15/mo...
    FLAT_RATE = "flat_rate"  # $5/user/mo
    SEAT = "seat"  # 1-10 users $5/user/mo, 11-30 users $4/user/mo


class ProductDAO(Base):
    __tablename__ = "products"

    id = Column(String(30), primary_key=True, default=generate_unique_key, index=True)
    account_id = Column(String(30), ForeignKey("accounts.id"), nullable=False)
    name = Column(String(100), nullable=False)

    trial_days = Column(SmallInteger(), default=0, nullable=False)
    cycle_days = Column(SmallInteger(), nullable=False)

    bulk_discount = Column(JSON())  # {days: percent_discount} {180: 5, 365: 10}

    added_at = Column(TIMESTAMP(), server_default=func.current_timestamp())
    deleted_at = Column(TIMESTAMP(), nullable=True)

    product_billing_types = relationship("ProductBillingTypeDAO", back_populates="product")

    __table_args__ = (
        UniqueConstraint("name", "account_id", name="uidx_account_id_name"),
    )


class ProductBillingTypeDAO(Base):
    __tablename__ = "product_billing_types"

    product_id = Column(String(30), ForeignKey("products.id"), primary_key=True)
    billing_type = Column(
        pg_enum(ProductBillingType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        primary_key=True,
    )

    product = relationship("ProductDAO", back_populates="product_billing_types")


class PlanDAO(Base):
    __tablename__ = "plans"

    id = Column(String(30), primary_key=True, default=generate_unique_key)
    name = Column(String(30), nullable=False)
    product_id = Column(
        String(30), ForeignKey("products.id"), nullable=False, index=True
    )
    features = Column(JSONB, nullable=False)
    base_price = Column(Numeric(precision=2), nullable=False)
    position = Column(SmallInteger(), nullable=False)

    __table_args__ = (
        UniqueConstraint("name", "product_id", name="uidx_product_id_name"),
    )


class ProductExtDAO(Base):
    __tablename__ = "products_ext"

    id = Column(String(30), primary_key=True, default=generate_unique_key)
    product_id = Column(String(30), ForeignKey("products.id"), nullable=False)
    label = Column(String(30), nullable=False)

    __table_args__ = (
        UniqueConstraint("label", "product_id", name="uidx_product_id_label"),
    )


class ChargeableDAO(Base):
    __tablename__ = "chargeables"

    id = Column(String(30), primary_key=True, default=generate_unique_key)
    plan_id = Column(String(30), ForeignKey("plans.id"), nullable=False)
    ext_id = Column(String(30), ForeignKey("products_ext.id"), nullable=False)
    value = Column(JSON(), nullable=True)
    #   volume - {'lower_limit': 1, 'upper_limit': 1000, 'price': 4}
    #   seat - {'lower_limit': 1, 'upper_limit': 10, 'price': 5} - this will charge for each seat

    __table_args__ = (
        UniqueConstraint("plan_id", "ext_id", name="uidx_plan_id_ext_id"),
    )
