from datetime import datetime

from pydantic import BaseModel

from src.data.products.db import ProductBillingType


class ProductBase(BaseModel):
    name: str
    billing_type: ProductBillingType
    trial_days: int
    cycle_days: int
    bulk_discount: dict


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: str
    added_at: datetime
    deleted_at: datetime | None = None

    class Config:
        use_enum_values = True
        orm_mode = True


class ProductExtBase(BaseModel):
    product_id: int
    label: str


class ProductExtBaseCreate(ProductExtBase):
    pass


class ProductExt(ProductExtBase):
    id: str


class Chargeable(BaseModel):
    field: str
    price: float
    lower_limit: int | None = None
    upper_limit: int | None = None


class PlanChargeableBase(BaseModel):
    plan_id: str
    ext_id: int
    value: Chargeable


class PlanBase(BaseModel):
    name: str
    base_price: float | None = None
    position: int
    chargeable: list[Chargeable]


class PlanCreate(PlanBase):
    pass


class Plan(PlanBase):
    product_id: str
