from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.api import accounts, users, products, customers
from src.data.base import Base, engine
from src.middleware import validate_domain

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=validate_domain)

app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(customers.router)
app.include_router(products.router)


@app.get("/")
async def root(request: Request):
    print(request.state.tenant_id)
    return {"message": f"Welcome to Bytes Lab Subscree"}
