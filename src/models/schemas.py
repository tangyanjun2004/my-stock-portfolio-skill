from typing import Optional
from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    name: str


class AccountCreate(AccountBase):
    balance: float = Field(..., ge=0)


class Account(AccountBase):
    id: int
    total_balance: float
    available_balance: float
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class PositionBase(BaseModel):
    stock_code: str
    stock_name: str


class PositionCreate(PositionBase):
    quantity: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    date: Optional[str] = None


class PositionUpdate(BaseModel):
    type: str = Field(..., pattern="^(buy|sell)$")
    quantity: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    date: Optional[str] = None


class Position(PositionBase):
    id: int
    account_id: int
    quantity: float
    average_cost: float
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class PositionDetail(Position):
    total_cost: float


class TransactionBase(BaseModel):
    stock_code: str
    stock_name: str
    type: str
    quantity: float
    price: float
    amount: float
    date: str
    note: Optional[str] = None


class Transaction(TransactionBase):
    id: int
    position_id: int
    created_at: str

    model_config = {"from_attributes": True}


class AccountTransactionBase(BaseModel):
    type: str
    amount: float
    note: Optional[str] = None


class AccountTransactionCreate(AccountTransactionBase):
    pass


class AccountTransaction(AccountTransactionBase):
    id: int
    account_id: int
    created_at: str

    model_config = {"from_attributes": True}


class WatchlistItemBase(BaseModel):
    stock_code: str
    stock_name: str


class WatchlistItemCreate(WatchlistItemBase):
    note: Optional[str] = None


class WatchlistItem(WatchlistItemBase):
    id: int
    note: Optional[str] = None
    created_at: str

    model_config = {"from_attributes": True}


class AccountInfo(BaseModel):
    account: Account
    total_position_value: float
    total_invested: float
    position_count: int
    available_balance: float
    total_balance: float
