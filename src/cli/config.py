import typer

from src.config import get_config
from src.utils.helpers import print_json

app = typer.Typer(name="config", help="配置查看")


@app.command("show")
def show_config():
    """显示当前配置"""
    config = get_config()

    from src.database.connection import get_db_path

    print_json({
        "config_file": config.config_file,
        "config_file_exists": config.config_file_exists,
        "db_path": config.db_path,
        "actual_db_path": get_db_path()
    })
