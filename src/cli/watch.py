import typer
from typing import Optional

from src.database.connection import get_session
from src.services.watchlist_service import WatchlistService
from src.models.schemas import WatchlistItemCreate
from src.utils.helpers import print_json

app = typer.Typer(name="watch", help="关注列表管理")


@app.command("add")
def add_to_watchlist(
    code: str = typer.Option(..., "--code", "-c", help="股票代码"),
    name: str = typer.Option(..., "--name", "-n", help="股票名称"),
    note: Optional[str] = typer.Option(None, "--note", help="备注")
):
    """添加到关注列表"""
    session = get_session()
    service = WatchlistService(session)
    try:
        item = service.add_to_watchlist(
            WatchlistItemCreate(stock_code=code, stock_name=name, note=note)
        )
        print_json({
            "watchlist_item": {
                "id": item.id,
                "stock_code": item.stock_code,
                "stock_name": item.stock_name,
                "note": item.note
            }
        }, message="添加成功")
    except ValueError as e:
        print_json(None, success=False, message=str(e))
        raise typer.Exit(1)
    finally:
        session.close()


@app.command("list")
def list_watchlist():
    """查看关注列表"""
    session = get_session()
    service = WatchlistService(session)
    try:
        items = service.get_watchlist()
        print_json({
            "watchlist": [
                {
                    "id": item.id,
                    "stock_code": item.stock_code,
                    "stock_name": item.stock_name,
                    "note": item.note,
                    "created_at": item.created_at
                }
                for item in items
            ]
        })
    finally:
        session.close()


@app.command("remove")
def remove_from_watchlist(identifier: str = typer.Argument(..., help="股票代码或ID")):
    """从关注列表移除"""
    session = get_session()
    service = WatchlistService(session)
    try:
        service.remove_from_watchlist(identifier)
        print_json({"identifier": identifier}, message="移除成功")
    except ValueError as e:
        print_json(None, success=False, message=str(e))
        raise typer.Exit(1)
    finally:
        session.close()
