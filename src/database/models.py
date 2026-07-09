from sqlalchemy import Column, Integer, String, Float, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


def get_current_time() -> str:
    return datetime.now().isoformat()


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    total_balance = Column(Float, nullable=False, default=0.0)
    available_balance = Column(Float, nullable=False, default=0.0)
    created_at = Column(String, nullable=False, default=get_current_time)
    updated_at = Column(String, nullable=False, default=get_current_time)

    positions = relationship("Position", back_populates="account", cascade="all, delete-orphan")
    account_transactions = relationship("AccountTransaction", back_populates="account", cascade="all, delete-orphan")


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    stock_code = Column(String, nullable=False)
    stock_name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    average_cost = Column(Float, nullable=False)
    created_at = Column(String, nullable=False, default=get_current_time)
    updated_at = Column(String, nullable=False, default=get_current_time)

    account = relationship("Account", back_populates="positions")
    transactions = relationship("Transaction", back_populates="position", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("account_id", "stock_code", name="uix_account_stock"),
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=False)
    type = Column(String, nullable=False)
    stock_code = Column(String, nullable=False)
    stock_name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(String, nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(String, nullable=False, default=get_current_time)

    position = relationship("Position", back_populates="transactions")

    __table_args__ = (
        CheckConstraint("type IN ('buy', 'sell')", name="ck_transaction_type"),
    )


class AccountTransaction(Base):
    __tablename__ = "account_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(String, nullable=False, default=get_current_time)

    account = relationship("Account", back_populates="account_transactions")

    __table_args__ = (
        CheckConstraint("type IN ('deposit', 'withdraw')", name="ck_account_transaction_type"),
    )


class WatchlistItem(Base):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String, nullable=False, unique=True)
    stock_name = Column(String, nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(String, nullable=False, default=get_current_time)
