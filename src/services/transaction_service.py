from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Transaction
from src.models.schemas import Transaction as TransactionSchema


class TransactionService:
    def __init__(self, session: Session):
        self.session = session

    def get_transactions(
        self,
        stock_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[TransactionSchema]:
        """获取交易记录"""
        query = self.session.query(Transaction)

        if stock_code:
            query = query.filter(Transaction.stock_code == stock_code)

        if start_date:
            query = query.filter(Transaction.date >= start_date)

        if end_date:
            query = query.filter(Transaction.date <= end_date)

        transactions = query.order_by(Transaction.date.desc(), Transaction.created_at.desc()).all()
        return [TransactionSchema.model_validate(t) for t in transactions]
