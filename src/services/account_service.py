from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from src.database.models import Account, AccountTransaction
from src.models.schemas import (
    Account as AccountSchema,
    AccountCreate,
    AccountTransaction as AccountTransactionSchema,
    AccountInfo
)
from src.utils.helpers import get_current_time


class AccountService:
    def __init__(self, session: Session):
        self.session = session

    def create_account(self, data: AccountCreate) -> AccountSchema:
        """创建账户"""
        existing = self.session.query(Account).first()
        if existing:
            raise ValueError("账户已存在，只能有一个账户")

        account = Account(
            name=data.name,
            total_balance=data.balance,
            available_balance=data.balance,
            created_at=get_current_time(),
            updated_at=get_current_time()
        )
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)
        return AccountSchema.model_validate(account)

    def get_account(self) -> Optional[AccountSchema]:
        """获取账户"""
        account = self.session.query(Account).first()
        if not account:
            return None
        return AccountSchema.model_validate(account)

    def get_account_info(self) -> Optional[AccountInfo]:
        """获取账户概览信息"""
        account = self.session.query(Account).first()
        if not account:
            return None

        from src.services.position_service import PositionService
        position_service = PositionService(self.session)
        positions = position_service.get_all_positions()

        total_invested = sum(p.average_cost * p.quantity for p in positions)
        position_count = len(positions)

        return AccountInfo(
            account=AccountSchema.model_validate(account),
            total_position_value=total_invested,
            total_invested=total_invested,
            position_count=position_count,
            available_balance=account.available_balance,
            total_balance=account.total_balance
        )

    def deposit(self, amount: float, note: Optional[str] = None) -> AccountSchema:
        """转入资金"""
        account = self.session.query(Account).first()
        if not account:
            raise ValueError("账户不存在，请先初始化账户")

        if amount <= 0:
            raise ValueError("转入金额必须大于0")

        account.total_balance += amount
        account.available_balance += amount
        account.updated_at = get_current_time()

        tx = AccountTransaction(
            account_id=account.id,
            type="deposit",
            amount=amount,
            note=note,
            created_at=get_current_time()
        )
        self.session.add(tx)
        self.session.commit()
        self.session.refresh(account)
        return AccountSchema.model_validate(account)

    def withdraw(self, amount: float, note: Optional[str] = None) -> AccountSchema:
        """转出资金"""
        account = self.session.query(Account).first()
        if not account:
            raise ValueError("账户不存在，请先初始化账户")

        if amount <= 0:
            raise ValueError("转出金额必须大于0")

        if amount > account.available_balance:
            raise ValueError(f"可用余额不足，当前可用: {account.available_balance}")

        account.total_balance -= amount
        account.available_balance -= amount
        account.updated_at = get_current_time()

        tx = AccountTransaction(
            account_id=account.id,
            type="withdraw",
            amount=amount,
            note=note,
            created_at=get_current_time()
        )
        self.session.add(tx)
        self.session.commit()
        self.session.refresh(account)
        return AccountSchema.model_validate(account)
