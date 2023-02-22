from fastapi import HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.auth import get_current_user

DOMAIN = "subscree.io"

# TODO - use redis to store mapping
TENANT_DOMAIN_USER_MAPPING = {
    "byteslab": {"id": 1, "users": {1, 2, 3, 4}},
    "percolate": {"id": 2, "users": {5, 6, 7}}
}

EXEMPTED_PATHS = ["/token"]


async def validate_domain(request: Request, call_next):
    request.state.tenant_id = None

    host = request.headers["host"]
    split_host = host.split(".", 1)
    subdomain, domain = split_host[0], split_host[1]

    if not domain == DOMAIN:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Not found."})

    tenant = TENANT_DOMAIN_USER_MAPPING.get(subdomain)
    if not tenant:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Invalid org."})

    if request.url.path in EXEMPTED_PATHS:
        return await call_next(request)

    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Token not provided."})

    try:
        current_user = await get_current_user(token=token[7:])
    except HTTPException:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Unauthorised."})

    if current_user.id not in tenant["users"]:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Unauthorized org."})

    request.state.tenant_id = tenant["id"]

    response = await call_next(request)

    return response
