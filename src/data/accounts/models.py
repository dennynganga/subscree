import datetime

from pydantic import BaseModel

from src.data.users.models import User


class AccountBase(BaseModel):
    name: str


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    # owner: User
    added_at: datetime.datetime

    class Config:
        orm_mode = True
