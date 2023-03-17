from fastapi import HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.auth import get_current_user

DOMAIN = "subscree.io"

# TODO - use redis to store mapping
TENANT_DOMAIN_USER_MAPPING = {
    "byteslab": {"id": "a3Kk4DcmFhEnwjatCiorKJ", "users": {"Evt3NcrcjPRU29b8rtn9wx"}},
    "percolate": {"id": 2, "users": {5, 6, 7}}
}

AUTH_EXEMPTED_PATHS = ["/token"]

PATHS_WITHOUT_TENANT = {"/accounts/": ["post"]}


async def validate_domain(request: Request, call_next):
    request.state.account_id = None

    path = request.url.path
    if path in PATHS_WITHOUT_TENANT and request.method.lower() in PATHS_WITHOUT_TENANT[path]:
        return await call_next(request)

    host = request.headers["host"]
    split_host = host.split(".", 1)
    subdomain, domain = split_host[0], split_host[1]

    if not domain == DOMAIN:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Not found."})

    account = TENANT_DOMAIN_USER_MAPPING.get(subdomain)
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Invalid org."})

    if path in AUTH_EXEMPTED_PATHS:
        return await call_next(request)

    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Token not provided."})

    try:
        current_user = await get_current_user(token=token[7:])
    except HTTPException:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Unauthorised."})

    if current_user.id not in account["users"]:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Unauthorized account."})

    request.state.account_id = account["id"]

    response = await call_next(request)

    return response
