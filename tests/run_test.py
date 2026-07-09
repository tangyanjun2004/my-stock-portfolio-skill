#!/usr/bin/env python3
"""运行测试"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.database.connection import get_session, init_db
from src.services.account_service import AccountService
from src.services.position_service import PositionService
from src.services.watchlist_service import WatchlistService
from src.models.schemas import AccountCreate, PositionCreate, WatchlistItemCreate

def main():
    print("=" * 60)
    print("简单功能测试")
    print("=" * 60)

    init_db()
    session = get_session()

    try:
        account_service = AccountService(session)

        # 尝试创建账户，如果已存在则获取
        try:
            account = account_service.create_account(AccountCreate(name="测试账户", balance=100000.0))
            print("账户创建成功！")
        except ValueError as e:
            if "已存在" in str(e):
                print("账户已存在，继续测试...")
            else:
                raise

        info = account_service.get_account_info()
        print(f"账户: {info.account.name}")
        print(f"总资产: {info.total_balance}")
        print(f"可用余额: {info.available_balance}")

        # 测试持仓
        position_service = PositionService(session)

        try:
            pos = position_service.add_position(
                PositionCreate(stock_code="600519", stock_name="贵州茅台", quantity=100, price=150.0)
            )
            print(f"添加持仓成功: {pos.stock_code}")
        except ValueError as e:
            print(f"添加持仓: {e}")

        positions = position_service.get_all_positions()
        print(f"当前持仓数量: {len(positions)}")
        for p in positions:
            print(f"  - {p.stock_code} {p.stock_name}: {p.quantity}")

        # 测试关注
        watch_service = WatchlistService(session)
        try:
            watch = watch_service.add_to_watchlist(
                WatchlistItemCreate(stock_code="AAPL", stock_name="苹果", note="关注")
            )
            print(f"添加关注成功: {watch.stock_code}")
        except ValueError as e:
            print(f"添加关注: {e}")

        watchlist = watch_service.get_watchlist()
        print(f"关注列表数量: {len(watchlist)}")

        print("\n测试成功！")

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    main()
