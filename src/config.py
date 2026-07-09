import json
from pathlib import Path
from typing import Optional
import sys


class Config:
    """配置管理"""

    def __init__(self):
        self.config_file = self._get_config_file_path()
        self._config = self._load_config()

    def _get_config_file_path(self) -> Path:
        """获取配置文件路径"""
        if getattr(sys, "frozen", False):
            # 打包后运行，使用 exe 同目录
            base_dir = Path(sys.executable).parent
        else:
            # 开发阶段，使用项目目录
            base_dir = Path(__file__).parent.parent

        return base_dir / "stock_portfolio_config.json"

    def _load_config(self) -> dict:
        """加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_config(self):
        """保存配置"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)

    @property
    def db_path(self) -> Optional[str]:
        """获取数据库路径"""
        return self._config.get("db_path")

    @db_path.setter
    def db_path(self, value: str):
        """设置数据库路径"""
        self._config["db_path"] = value
        self._save_config()

    @property
    def config_file_exists(self) -> bool:
        """配置文件是否存在"""
        return self.config_file.exists()


# 全局配置实例
_config_instance = None


def get_config() -> Config:
    """获取配置实例"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
