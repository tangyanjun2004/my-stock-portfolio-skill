import typer
from typing import Optional

from src.database.connection import get_session
from src.services.transaction_service import TransactionService
from src.utils.helpers import format_currency, format_quantity, print_json

app = typer.Typer(name="transaction", help="交易记录查询")


@app.command("list")
def list_transactions(
    stock: Optional[str] = typer.Option(None, "--stock", "-s", help="股票代码"),
    start: Optional[str] = typer.Option(None, "--start", help="开始日期 (YYYY-MM-DD)"),
    end: Optional[str] = typer.Option(None, "--end", help="结束日期 (YYYY-MM-DD)")
):
    """查看交易记录"""
    session = get_session()
    service = TransactionService(session)
    try:
        transactions = service.get_transactions(stock_code=stock, start_date=start, end_date=end)
        print_json({
            "transactions": [
                {
                    "id": t.id,
                    "date": t.date,
                    "type": t.type,
                    "stock_code": t.stock_code,
                    "stock_name": t.stock_name,
                    "quantity": t.quantity,
                    "price": t.price,
                    "amount": t.amount
                }
                for t in transactions
            ]
        })
    finally:
        session.close()
