import pytest
from src.services.account_service import AccountService
from src.models.schemas import AccountCreate


class TestAccountService:
    def test_create_account(self, db_session):
        service = AccountService(db_session)
        account = service.create_account(AccountCreate(name="测试账户", balance=10000.0))

        assert account.name == "测试账户"
        assert account.total_balance == 10000.0
        assert account.available_balance == 10000.0

    def test_create_duplicate_account(self, db_session):
        service = AccountService(db_session)
        service.create_account(AccountCreate(name="测试账户", balance=10000.0))

        with pytest.raises(ValueError, match="账户已存在"):
            service.create_account(AccountCreate(name="另一个账户", balance=5000.0))

    def test_deposit(self, db_session):
        service = AccountService(db_session)
        service.create_account(AccountCreate(name="测试账户", balance=10000.0))

        account = service.deposit(5000.0, "转入测试")
        assert account.available_balance == 15000.0
        assert account.total_balance == 15000.0

    def test_withdraw(self, db_session):
        service = AccountService(db_session)
        service.create_account(AccountCreate(name="测试账户", balance=10000.0))

        account = service.withdraw(3000.0, "转出测试")
        assert account.available_balance == 7000.0
        assert account.total_balance == 7000.0

    def test_withdraw_insufficient_balance(self, db_session):
        service = AccountService(db_session)
        service.create_account(AccountCreate(name="测试账户", balance=1000.0))

        with pytest.raises(ValueError, match="可用余额不足"):
            service.withdraw(2000.0)

    def test_get_account_info(self, db_session):
        service = AccountService(db_session)
        service.create_account(AccountCreate(name="测试账户", balance=10000.0))

        info = service.get_account_info()
        assert info is not None
        assert info.account.name == "测试账户"
