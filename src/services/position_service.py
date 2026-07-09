from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from src.database.models import Position, Transaction, Account
from src.models.schemas import (
    Position as PositionSchema,
    PositionCreate,
    PositionUpdate,
    PositionDetail
)
from src.utils.helpers import get_current_time, format_date


class PositionService:
    def __init__(self, session: Session):
        self.session = session

    def _get_account(self) -> Account:
        account = self.session.query(Account).first()
        if not account:
            raise ValueError("账户不存在，请先初始化账户")
        return account

    def add_position(self, data: PositionCreate) -> PositionSchema:
        """添加持仓"""
        account = self._get_account()

        total_cost = data.quantity * data.price
        if total_cost > account.available_balance:
            raise ValueError(f"可用余额不足，需要: {total_cost}, 当前可用: {account.available_balance}")

        existing = self.session.query(Position).filter(
            Position.account_id == account.id,
            Position.stock_code == data.stock_code
        ).first()

        if existing:
            raise ValueError(f"股票 {data.stock_code} 已存在持仓，请使用 update 命令")

        position = Position(
            account_id=account.id,
            stock_code=data.stock_code,
            stock_name=data.stock_name,
            quantity=data.quantity,
            average_cost=data.price,
            created_at=get_current_time(),
            updated_at=get_current_time()
        )
        self.session.add(position)
        self.session.flush()

        tx = Transaction(
            position_id=position.id,
            type="buy",
            stock_code=data.stock_code,
            stock_name=data.stock_name,
            quantity=data.quantity,
            price=data.price,
            amount=total_cost,
            date=format_date(data.date),
            created_at=get_current_time()
        )
        self.session.add(tx)

        account.available_balance -= total_cost
        account.updated_at = get_current_time()

        self.session.commit()
        self.session.refresh(position)
        return PositionSchema.model_validate(position)

    def update_position(self, identifier: str, data: PositionUpdate) -> PositionSchema:
        """更新持仓（买入/卖出）"""
        account = self._get_account()

        position = self._get_position_by_identifier(account.id, identifier)
        if not position:
            raise ValueError(f"未找到持仓: {identifier}")

        tx_amount = data.quantity * data.price

        if data.type == "buy":
            if tx_amount > account.available_balance:
                raise ValueError(f"可用余额不足，需要: {tx_amount}, 当前可用: {account.available_balance}")

            total_quantity = position.quantity + data.quantity
            total_cost = (position.quantity * position.average_cost) + tx_amount
            new_average_cost = total_cost / total_quantity

            position.quantity = total_quantity
            position.average_cost = new_average_cost
            account.available_balance -= tx_amount

        else:  # sell
            if data.quantity > position.quantity:
                raise ValueError(f"持仓数量不足，当前持有: {position.quantity}")

            position.quantity -= data.quantity
            account.available_balance += tx_amount

            if position.quantity == 0:
                self.session.delete(position)

        tx = Transaction(
            position_id=position.id if position.quantity > 0 else 0,
            type=data.type,
            stock_code=position.stock_code,
            stock_name=position.stock_name,
            quantity=data.quantity,
            price=data.price,
            amount=tx_amount,
            date=format_date(data.date),
            created_at=get_current_time()
        )
        self.session.add(tx)

        if position.quantity > 0:
            position.updated_at = get_current_time()

        account.updated_at = get_current_time()
        self.session.commit()

        if position.quantity > 0:
            self.session.refresh(position)
            return PositionSchema.model_validate(position)
        else:
            return None

    def remove_position(self, identifier: str) -> bool:
        """删除持仓"""
        account = self._get_account()
        position = self._get_position_by_identifier(account.id, identifier)
        if not position:
            raise ValueError(f"未找到持仓: {identifier}")

        locked_value = position.quantity * position.average_cost
        account.available_balance += locked_value
        account.updated_at = get_current_time()

        self.session.delete(position)
        self.session.commit()
        return True

    def get_position(self, identifier: str) -> Optional[PositionDetail]:
        """获取单个持仓详情"""
        account = self.session.query(Account).first()
        if not account:
            return None

        position = self._get_position_by_identifier(account.id, identifier)
        if not position:
            return None

        return PositionDetail(
            id=position.id,
            account_id=position.account_id,
            stock_code=position.stock_code,
            stock_name=position.stock_name,
            quantity=position.quantity,
            average_cost=position.average_cost,
            total_cost=position.quantity * position.average_cost,
            created_at=position.created_at,
            updated_at=position.updated_at
        )

    def get_all_positions(self) -> List[PositionSchema]:
        """获取所有持仓"""
        account = self.session.query(Account).first()
        if not account:
            return []

        positions = self.session.query(Position).filter(Position.account_id == account.id).all()
        return [PositionSchema.model_validate(p) for p in positions]

    def _get_position_by_identifier(self, account_id: int, identifier: str) -> Optional[Position]:
        """通过股票代码或ID查找持仓"""
        if identifier.isdigit():
            return self.session.query(Position).filter(
                Position.account_id == account_id,
                Position.id == int(identifier)
            ).first()
        else:
            return self.session.query(Position).filter(
                Position.account_id == account_id,
                Position.stock_code == identifier
            ).first()
