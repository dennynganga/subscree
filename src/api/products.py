from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

from src.api.utils import object_belongs_to_account
from src.data.base import session_scope
from src.data.products import models as product_models, crud as products_crud

router = APIRouter()


@router.post("/products", response_model=product_models.Product)
def create_product(
    request: Request,
    product: product_models.ProductCreate,
    session: Session = Depends(session_scope),
):
    account_id = request.state.account_id
    product_exists = products_crud.retrieve_product_by_name(
        name=product.name, account_id=account_id, session=session
    )
    if product_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product with name '{product.name}' already exists.",
        )
    return products_crud.add_product(
        product=product, account_id=account_id, session=session
    )


@router.get("/products", response_model=list[product_models.Product])
def get_products(request: Request, session: Session = Depends(session_scope)):
    account_id = request.state.account_id
    return products_crud.retrieve_products(account_id=account_id, session=session)


@router.get("/products/{product_id}", response_model=product_models.Product)
def get_product(
    product_id: str, request: Request, session: Session = Depends(session_scope)
):
    account_id = request.state.account_id
    product = products_crud.retrieve_product_by_id(
        account_id=account_id, product_id=product_id, session=session
    )
    return product


@router.put("/products/{product_id}", response_model=product_models.Product)
def update_product(
    product_id: str, request: Request, session: Session = Depends(session_scope)
):
    account_id = request.state.account_id
    product = products_crud.retrieve_product_by_id(
        account_id=account_id, product_id=product_id, session=session
    )
    return products_crud.update_product(product_id=product.id, session=session)


@router.post("/products/{product_id}/plans", response_model=product_models.Plan)
def add_plan(
    request: Request,
    product_id: str,
    plan: product_models.PlanCreate,
    session: Session = Depends(session_scope),
):
    account_id = request.state.account_id
    product = products_crud.retrieve_product_by_id(
        account_id=account_id, product_id=product_id, session=session
    )
    return products_crud.add_plan(
        account_id=account_id, product_id=product.id, plan=plan, session=session
    )


@router.get("/products/{product_id}/plans", response_model=list[product_models.Plan])
def get_product_plans(
    request: Request, product_id: str, session: Session = Depends(session_scope)
):
    account_id = request.state.account_id
    product = products_crud.retrieve_product_by_id(
        account_id=account_id, product_id=product_id, session=session
    )
    return products_crud.get_product_plans(product_id=product.id, session=session)
