import typer
from typing import Optional

from src.database.connection import get_session
from src.services.position_service import PositionService
from src.models.schemas import PositionCreate, PositionUpdate
from src.utils.helpers import format_currency, format_quantity, print_json

app = typer.Typer(name="position", help="持仓管理")


@app.command("add")
def add_position(
    code: str = typer.Option(..., "--code", "-c", help="股票代码"),
    name: str = typer.Option(..., "--name", "-n", help="股票名称"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="数量"),
    price: float = typer.Option(..., "--price", "-p", help="价格"),
    date: Optional[str] = typer.Option(None, "--date", "-d", help="日期 (YYYY-MM-DD)")
):
    """添加持仓"""
    session = get_session()
    service = PositionService(session)
    try:
        position = service.add_position(
            PositionCreate(stock_code=code, stock_name=name, quantity=quantity, price=price, date=date)
        )
        print_json({
            "position": {
                "id": position.id,
                "stock_code": position.stock_code,
                "stock_name": position.stock_name,
                "quantity": position.quantity,
                "average_cost": position.average_cost
            }
        }, message="持仓添加成功")
    except ValueError as e:
        print_json(None, success=False, message=str(e))
        raise typer.Exit(1)
    finally:
        session.close()


@app.command("list")
def list_positions():
    """查看持仓列表"""
    session = get_session()
    service = PositionService(session)
    try:
        positions = service.get_all_positions()
        print_json({
            "positions": [
                {
                    "id": p.id,
                    "stock_code": p.stock_code,
                    "stock_name": p.stock_name,
                    "quantity": p.quantity,
                    "average_cost": p.average_cost,
                    "market_value": p.quantity * p.average_cost
                }
                for p in positions
            ]
        })
    finally:
        session.close()


@app.command("show")
def show_position(identifier: str = typer.Argument(..., help="股票代码或ID")):
    """查看单个持仓详情"""
    session = get_session()
    service = PositionService(session)
    try:
        position = service.get_position(identifier)
        if not position:
            print_json(None, success=False, message=f"未找到持仓: {identifier}")
            raise typer.Exit(1)

        print_json({
            "position": {
                "id": position.id,
                "stock_code": position.stock_code,
                "stock_name": position.stock_name,
                "quantity": position.quantity,
                "average_cost": position.average_cost,
                "total_cost": position.total_cost,
                "created_at": position.created_at,
                "updated_at": position.updated_at
            }
        })
    finally:
        session.close()


@app.command("update")
def update_position(
    identifier: str = typer.Argument(..., help="股票代码或ID"),
    type: str = typer.Option(..., "--type", "-t", help="交易类型 (buy/sell)"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="数量"),
    price: float = typer.Option(..., "--price", "-p", help="价格"),
    date: Optional[str] = typer.Option(None, "--date", "-d", help="日期 (YYYY-MM-DD)")
):
    """更新持仓（买入/卖出）"""
    session = get_session()
    service = PositionService(session)
    try:
        position = service.update_position(
            identifier,
            PositionUpdate(type=type, quantity=quantity, price=price, date=date)
        )
        if position:
            print_json({
                "position": {
                    "id": position.id,
                    "stock_code": position.stock_code,
                    "stock_name": position.stock_name,
                    "quantity": position.quantity,
                    "average_cost": position.average_cost
                }
            }, message="更新成功")
        else:
            print_json({"position_removed": True}, message="持仓已清空并删除")
    except ValueError as e:
        print_json(None, success=False, message=str(e))
        raise typer.Exit(1)
    finally:
        session.close()


@app.command("remove")
def remove_position(identifier: str = typer.Argument(..., help="股票代码或ID")):
    """删除持仓"""
    session = get_session()
    service = PositionService(session)
    try:
        service.remove_position(identifier)
        print_json({"identifier": identifier}, message="删除成功")
    except ValueError as e:
        print_json(None, success=False, message=str(e))
        raise typer.Exit(1)
    finally:
        session.close()
