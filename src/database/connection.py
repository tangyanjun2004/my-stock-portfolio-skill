import os
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base
from src.config import get_config


def get_data_dir() -> Path:
    """获取数据存储目录"""
    config = get_config()

    # 优先使用配置文件中的路径
    if config.db_path:
        db_path = Path(config.db_path)
        if db_path.is_dir():
            data_dir = db_path
        else:
            data_dir = db_path.parent
    else:
        # 默认路径
        if getattr(sys, "frozen", False):
            # 打包后运行，使用用户目录
            data_dir = Path.home() / ".stock_portfolio"
        else:
            # 开发阶段，使用项目目录
            data_dir = Path(__file__).parent.parent.parent / "data"

    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_db_path() -> Path:
    """获取数据库文件路径"""
    config = get_config()

    if config.db_path:
        db_path = Path(config.db_path)
        if not db_path.is_dir():
            return db_path

    return get_data_dir() / "portfolio.db"


def get_db_url() -> str:
    """获取数据库连接 URL"""
    db_path = get_db_path()
    return f"sqlite:///{db_path}"


# 全局 engine 和 session factory
_engine = None
_SessionLocal = None


def init_db() -> None:
    """初始化数据库连接和表"""
    global _engine, _SessionLocal

    if _engine is None:
        db_url = get_db_url()
        _engine = create_engine(db_url, connect_args={"check_same_thread": False})
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

        # 创建表
        Base.metadata.create_all(bind=_engine)


def get_session() -> Session:
    """获取数据库会话"""
    if _engine is None:
        init_db()
    return _SessionLocal()


def get_engine():
    """获取数据库 engine"""
    if _engine is None:
        init_db()
    return _engine
