import typer
import json

from src import __version__
from src.cli import account, position, transaction, watch, config

app = typer.Typer(name="stock", help="股票投资组合管理")
app.add_typer(account.app)
app.add_typer(position.app)
app.add_typer(transaction.app)
app.add_typer(watch.app)
app.add_typer(config.app)


def version_callback(value: bool):
    if value:
        print(json.dumps({
            "success": True,
            "data": {
                "name": "stock-portfolio-cli",
                "version": __version__
            }
        }, ensure_ascii=False))
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", "-v", callback=version_callback, help="显示版本"
    )
):
    pass


if __name__ == "__main__":
    app()
