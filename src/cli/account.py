import typer
from typing import Optional

from src.database.connection import get_session
from src.services.account_service import AccountService
from src.models.schemas import AccountCreate
from src.utils.helpers import format_currency, print_json

app = typer.Typer(name="account", help="账户管理")


@app.command("init")
def init_account(
    name: str = typer.Option(..., "--name", "-n", help="账户名称"),
    balance: float = typer.Option(..., "--balance", "-b", help="初始金额")
):
    """初始化账户"""
    session = get_session()
    service = AccountService(session)
    try:
        account = service.create_account(AccountCreate(name=name, balance=balance))
        print_json({
            "account": {
                "id": account.id,
                "name": account.name,
                "total_balance": account.total_balance,
                "available_balance": account.available_balance
            }
        }, message="账户创建成功")
    except ValueError as e:
        print_json(None, success=False, message=str(e))
        raise typer.Exit(1)
    finally:
        session.close()


@app.command("info")
def account_info():
    """查看账户概览"""
    session = get_session()
    service = AccountService(session)
    try:
        info = service.get_account_info()
        if not info:
            print_json(None, success=False, message="账户不存在，请先使用 'account init' 初始化账户")
            raise typer.Exit(1)

        print_json({
            "account": {
                "id": info.account.id,
                "name": info.account.name,
                "total_balance": info.total_balance,
                "available_balance": info.available_balance,
                "total_position_value": info.total_position_value,
                "position_count": info.position_count
            }
        })
    finally:
        session.close()


@app.command("deposit")
def deposit(
    amount: float = typer.Argument(..., help="转入金额"),
    note: Optional[str] = typer.Option(None, "--note", "-n", help="备注")
):
    """转入资金"""
    session = get_session()
    service = AccountService(session)
    try:
        account = service.deposit(amount, note)
        print_json({
            "account": {
                "id": account.id,
                "name": account.name,
                "total_balance": account.total_balance,
                "available_balance": account.available_balance
            },
            "deposit_amount": amount,
            "note": note
        }, message="转入成功")
    except ValueError as e:
        print_json(None, success=False, message=str(e))
        raise typer.Exit(1)
    finally:
        session.close()


@app.command("withdraw")
def withdraw(
    amount: float = typer.Argument(..., help="转出金额"),
    note: Optional[str] = typer.Option(None, "--note", "-n", help="备注")
):
    """转出资金"""
    session = get_session()
    service = AccountService(session)
    try:
        account = service.withdraw(amount, note)
        print_json({
            "account": {
                "id": account.id,
                "name": account.name,
                "total_balance": account.total_balance,
                "available_balance": account.available_balance
            },
            "withdraw_amount": amount,
            "note": note
        }, message="转出成功")
    except ValueError as e:
        print_json(None, success=False, message=str(e))
        raise typer.Exit(1)
    finally:
        session.close()
