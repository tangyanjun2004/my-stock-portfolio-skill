#!/usr/bin/env python3
"""
简单演示脚本，验证基本功能
"""

import sys
from pathlib import Path

# 确保能找到 stock_portfolio 模块
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.database.connection import get_session, init_db
from src.services.account_service import AccountService
from src.services.position_service import PositionService
from src.services.watchlist_service import WatchlistService
from src.models.schemas import AccountCreate, PositionCreate, WatchlistItemCreate


def main():
    print("=" * 60)
    print("股票投资组合 Skill - 功能演示")
    print("=" * 60)

    # 初始化数据库
    init_db()
    session = get_session()

    try:
        print("\n1. 初始化账户...")
        account_service = AccountService(session)
        account = account_service.create_account(AccountCreate(name="演示账户", balance=100000.0))
        print(f"   ✓ 账户创建成功: {account.name}, 初始资金: {account.total_balance}")

        print("\n2. 添加持仓...")
        position_service = PositionService(session)
        pos1 = position_service.add_position(
            PositionCreate(stock_code="600519", stock_name="贵州茅台", quantity=100, price=150.0)
        )
        print(f"   ✓ 添加持仓: {pos1.stock_code} {pos1.stock_name}")

        pos2 = position_service.add_position(
            PositionCreate(stock_code="000001", stock_name="平安银行", quantity=500, price=10.0)
        )
        print(f"   ✓ 添加持仓: {pos2.stock_code} {pos2.stock_name}")

        print("\n3. 添加关注...")
        watch_service = WatchlistService(session)
        watch1 = watch_service.add_to_watchlist(
            WatchlistItemCreate(stock_code="AAPL", stock_name="苹果公司", note="关注中")
        )
        print(f"   ✓ 添加关注: {watch1.stock_code} {watch1.stock_name}")

        print("\n4. 查询账户信息...")
        info = account_service.get_account_info()
        print(f"   ✓ 账户总资产: {info.total_balance}")
        print(f"   ✓ 可用余额: {info.available_balance}")
        print(f"   ✓ 持仓数量: {info.position_count}")

        print("\n" + "=" * 60)
        print("演示完成!")
        print("=" * 60)
        print("\n你现在可以使用以下命令:")
        print("  python -m stock_portfolio account info   - 查看账户")
        print("  python -m stock_portfolio position list  - 查看持仓")
        print("  python -m stock_portfolio watch list     - 查看关注列表")

    except ValueError as e:
        if "账户已存在" in str(e):
            print("\n账户已存在，跳过初始化，直接查询...")
            info = account_service.get_account_info()
            if info:
                print(f"  账户: {info.account.name}")
                print(f"  总资产: {info.total_balance}")
        else:
            print(f"\n错误: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
