import pytest
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base


@pytest.fixture
def temp_db(tmp_path):
    """创建临时数据库"""
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield SessionLocal

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(temp_db):
    """获取数据库会话"""
    session = temp_db()
    yield session
    session.rollback()
    session.close()
