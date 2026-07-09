#!/usr/bin/env python3
"""批量更新导入语句"""

import re
from pathlib import Path

def update_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换 from stock_portfolio import -> from src import
    new_content = re.sub(r'from stock_portfolio', 'from src', content)
    # 替换 import stock_portfolio -> import src (如果有的话)
    new_content = re.sub(r'import stock_portfolio', 'import src', new_content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {file_path}")
    else:
        print(f"Skipped (no changes): {file_path}")

def main():
    project_root = Path(__file__).parent

    # 更新 src 目录下的所有 Python 文件
    src_dir = project_root / "src"
    for py_file in src_dir.rglob("*.py"):
        update_file(py_file)

    # 更新 tests 目录下的所有 Python 文件
    tests_dir = project_root / "tests"
    if tests_dir.exists():
        for py_file in tests_dir.rglob("*.py"):
            update_file(py_file)

    # 更新根目录下的测试文件
    for filename in ["test_demo.py", "simple_test.py"]:
        file_path = project_root / filename
        if file_path.exists():
            update_file(file_path)

    # 更新 build.py
    build_file = project_root / "build.py"
    if build_file.exists():
        update_file(build_file)

    print("\nImport update complete!")

if __name__ == "__main__":
    main()
