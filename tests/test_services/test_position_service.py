import pytest
from src.services.account_service import AccountService
from src.services.position_service import PositionService
from src.models.schemas import AccountCreate, PositionCreate, PositionUpdate


class TestPositionService:
    def test_add_position(self, db_session):
        account_service = AccountService(db_session)
        account_service.create_account(AccountCreate(name="测试账户", balance=10000.0))

        service = PositionService(db_session)
        position = service.add_position(
            PositionCreate(stock_code="600519", stock_name="贵州茅台", quantity=100, price=50.0)
        )

        assert position.stock_code == "600519"
        assert position.quantity == 100
        assert position.average_cost == 50.0

        account = account_service.get_account()
        assert account.available_balance == 5000.0

    def test_add_position_insufficient_balance(self, db_session):
        account_service = AccountService(db_session)
        account_service.create_account(AccountCreate(name="测试账户", balance=1000.0))

        service = PositionService(db_session)

        with pytest.raises(ValueError, match="可用余额不足"):
            service.add_position(
                PositionCreate(stock_code="600519", stock_name="贵州茅台", quantity=100, price=50.0)
            )

    def test_update_position_buy(self, db_session):
        account_service = AccountService(db_session)
        account_service.create_account(AccountCreate(name="测试账户", balance=10000.0))

        service = PositionService(db_session)
        service.add_position(
            PositionCreate(stock_code="600519", stock_name="贵州茅台", quantity=100, price=50.0)
        )

        position = service.update_position(
            "600519",
            PositionUpdate(type="buy", quantity=100, price=60.0)
        )

        assert position.quantity == 200
        assert position.average_cost == 55.0

    def test_update_position_sell(self, db_session):
        account_service = AccountService(db_session)
        account_service.create_account(AccountCreate(name="测试账户", balance=10000.0))

        service = PositionService(db_session)
        service.add_position(
            PositionCreate(stock_code="600519", stock_name="贵州茅台", quantity=100, price=50.0)
        )

        position = service.update_position(
            "600519",
            PositionUpdate(type="sell", quantity=50, price=60.0)
        )

        assert position.quantity == 50

    def test_get_all_positions(self, db_session):
        account_service = AccountService(db_session)
        account_service.create_account(AccountCreate(name="测试账户", balance=100000.0))

        service = PositionService(db_session)
        service.add_position(
            PositionCreate(stock_code="600519", stock_name="贵州茅台", quantity=100, price=50.0)
        )
        service.add_position(
            PositionCreate(stock_code="000001", stock_name="平安银行", quantity=200, price=20.0)
        )

        positions = service.get_all_positions()
        assert len(positions) == 2
