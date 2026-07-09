from typing import Optional, Any
from datetime import datetime
import json


def get_current_time() -> str:
    """获取当前时间的 ISO 格式字符串"""
    return datetime.now().isoformat()


def format_date(date_str: Optional[str] = None) -> str:
    """格式化日期，如果没有提供则使用当前日期"""
    if date_str:
        return date_str
    return datetime.now().date().isoformat()


def format_currency(amount: float) -> str:
    """格式化金额显示"""
    return f"{amount:,.2f}"


def format_quantity(quantity: float) -> str:
    """格式化数量显示"""
    if quantity.is_integer():
        return f"{int(quantity)}"
    return f"{quantity:,.4f}"


def print_json(data: Any, success: bool = True, message: Optional[str] = None):
    """打印 JSON 格式的输出"""
    output = {
        "success": success,
        "data": data
    }
    if message:
        output["message"] = message
    print(json.dumps(output, ensure_ascii=False, default=str))
