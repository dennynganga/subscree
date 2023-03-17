from starlette import status
from starlette.exceptions import HTTPException


def object_belongs_to_account(obj, account_id):
    if getattr(obj, "account_id") != account_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
