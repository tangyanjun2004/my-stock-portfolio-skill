from typing import List, Optional
from sqlalchemy.orm import Session

from src.database.models import WatchlistItem
from src.models.schemas import (
    WatchlistItem as WatchlistItemSchema,
    WatchlistItemCreate
)
from src.utils.helpers import get_current_time


class WatchlistService:
    def __init__(self, session: Session):
        self.session = session

    def add_to_watchlist(self, data: WatchlistItemCreate) -> WatchlistItemSchema:
        """添加到关注列表"""
        existing = self.session.query(WatchlistItem).filter(
            WatchlistItem.stock_code == data.stock_code
        ).first()

        if existing:
            raise ValueError(f"股票 {data.stock_code} 已在关注列表中")

        item = WatchlistItem(
            stock_code=data.stock_code,
            stock_name=data.stock_name,
            note=data.note,
            created_at=get_current_time()
        )
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return WatchlistItemSchema.model_validate(item)

    def remove_from_watchlist(self, identifier: str) -> bool:
        """从关注列表移除"""
        item = self._get_item_by_identifier(identifier)
        if not item:
            raise ValueError(f"未找到关注项: {identifier}")

        self.session.delete(item)
        self.session.commit()
        return True

    def get_watchlist(self) -> List[WatchlistItemSchema]:
        """获取关注列表"""
        items = self.session.query(WatchlistItem).order_by(WatchlistItem.created_at.desc()).all()
        return [WatchlistItemSchema.model_validate(item) for item in items]

    def _get_item_by_identifier(self, identifier: str) -> Optional[WatchlistItem]:
        """通过股票代码或ID查找关注项"""
        if identifier.isdigit():
            return self.session.query(WatchlistItem).filter(
                WatchlistItem.id == int(identifier)
            ).first()
        else:
            return self.session.query(WatchlistItem).filter(
                WatchlistItem.stock_code == identifier
            ).first()
