import pytest
from src.services.watchlist_service import WatchlistService
from src.models.schemas import WatchlistItemCreate


class TestWatchlistService:
    def test_add_to_watchlist(self, db_session):
        service = WatchlistService(db_session)
        item = service.add_to_watchlist(
            WatchlistItemCreate(stock_code="600519", stock_name="贵州茅台", note="关注")
        )

        assert item.stock_code == "600519"
        assert item.stock_name == "贵州茅台"
        assert item.note == "关注"

    def test_add_duplicate(self, db_session):
        service = WatchlistService(db_session)
        service.add_to_watchlist(
            WatchlistItemCreate(stock_code="600519", stock_name="贵州茅台")
        )

        with pytest.raises(ValueError, match="已在关注列表中"):
            service.add_to_watchlist(
                WatchlistItemCreate(stock_code="600519", stock_name="贵州茅台")
            )

    def test_get_watchlist(self, db_session):
        service = WatchlistService(db_session)
        service.add_to_watchlist(
            WatchlistItemCreate(stock_code="600519", stock_name="贵州茅台")
        )
        service.add_to_watchlist(
            WatchlistItemCreate(stock_code="000001", stock_name="平安银行")
        )

        items = service.get_watchlist()
        assert len(items) == 2

    def test_remove_from_watchlist(self, db_session):
        service = WatchlistService(db_session)
        service.add_to_watchlist(
            WatchlistItemCreate(stock_code="600519", stock_name="贵州茅台")
        )

        result = service.remove_from_watchlist("600519")
        assert result is True

        items = service.get_watchlist()
        assert len(items) == 0
