from sqlalchemy.orm import Session

from src.data.products.db import ProductDAO
from src.data.products.models import ProductCreate, PlanCreate


def add_product(product: ProductCreate, account_id: str, session: Session):
    product_dict = product.dict()
    product_dict.update({"account_id": account_id})
    product_dict.pop("product_billing_types")
    print(product_dict)
    new_product = ProductDAO(**product.dict())
    session.add(new_product)
    session.flush()
    session.refresh(new_product)
    return new_product


def retrieve_products(account_id: str, session: Session) :
    products = (
        session.query(ProductDAO).filter(ProductDAO.account_id == account_id).all()
    )
    return products


def retrieve_product_by_id(account_id: str, product_id: str, session: Session):
    return (
        session.query(ProductDAO)
        .filter(ProductDAO.account_id == account_id, ProductDAO.id == product_id)
        .first()
    )


def retrieve_product_by_name(name: str, account_id: str, session: Session):
    return (
        session.query(ProductDAO)
        .filter(ProductDAO.name == name, ProductDAO.account_id == account_id)
        .first()
    )


def update_product(product_id: str, session: Session):
    product = retrieve_product_by_id(product_id=product_id, session=session)


def add_plan(account_id: str, product_id: str, plan: PlanCreate, session: Session):
    pass


def get_plan_by_id(plan_id: str, session: Session):
    pass


def get_product_plans(product_id: str, session: Session):
    pass
