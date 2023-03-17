import datetime

from pydantic import BaseModel

from src.data.users.models import User, UserCreate


class AccountBase(BaseModel):
    name: str
    country: str


class AccountCreate(AccountBase):
    owner_id: str | None = None
    owner: UserCreate | None = None


class Account(AccountBase):
    id: str
    # owner: User
    added_at: datetime.datetime

    class Config:
        orm_mode = True
