import os
import sys
import shutil
from pathlib import Path
import PyInstaller.__main__

PROJECT_ROOT = Path(__file__).parent
DIST_DIR = PROJECT_ROOT / "dist"
BIN_DIR = DIST_DIR / "bin"
DOCS_OUTPUT_DIR = PROJECT_ROOT / "docs" / "output"


def clean_build():
    """清理旧的构建产物"""
    import time
    max_retries = 3
    for retry in range(max_retries):
        try:
            if DIST_DIR.exists():
                shutil.rmtree(DIST_DIR)
            build_dir = PROJECT_ROOT / "build"
            if build_dir.exists():
                shutil.rmtree(build_dir)
            spec_file = PROJECT_ROOT / "my-stock-portfolio-cli.spec"
            if spec_file.exists():
                spec_file.unlink()
            break
        except PermissionError:
            if retry < max_retries - 1:
                print(f"文件被占用，等待后重试... ({retry + 1}/{max_retries})")
                time.sleep(1)
            else:
                print("警告: 无法完全清理旧构建文件，请关闭正在运行的程序后重试")


def build_exe():
    """构建可执行文件"""
    BIN_DIR.mkdir(parents=True, exist_ok=True)

    exe_name = "my-stock-portfolio-cli"
    if sys.platform == "win32":
        exe_name += ".exe"

    PyInstaller.__main__.run([
        "--name=my-stock-portfolio-cli",
        "--onefile",
        f"--distpath={BIN_DIR}",
        "--clean",
        str(PROJECT_ROOT / "src" / "__main__.py")
    ])


def copy_docs():
    """复制文档文件"""
    # 复制 SKILL.md
    skill_md = DOCS_OUTPUT_DIR / "SKILL.md"
    if skill_md.exists():
        shutil.copy(skill_md, DIST_DIR / "SKILL.md")
        print(f"Copied: SKILL.md")

    # 复制配置示例文件到 bin 目录
    config_example = DOCS_OUTPUT_DIR / "stock_portfolio_config.json.example"
    if config_example.exists():
        shutil.copy(config_example, BIN_DIR / "stock_portfolio_config.json.example")
        print(f"Copied: stock_portfolio_config.json.example to bin/")

    # 创建配置说明文档到 bin 目录，命名为 README.txt
    readme_content = """配置说明
========

1. 复制示例配置文件并修改：
   copy stock_portfolio_config.json.example stock_portfolio_config.json

2. 编辑 stock_portfolio_config.json，设置 db_path

3. db_path 可以是：
   - 数据库文件路径（如：portfolio.db 或 C:/data/stock.db）
   - 目录路径（如：./data，会在目录下创建 portfolio.db）

4. 如果不配置，默认使用用户目录下的 .stock_portfolio 文件夹

5. 使用 "my-stock-portfolio-cli config show" 命令查看当前配置

详细使用说明请查看 ../SKILL.md
"""
    with open(BIN_DIR / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"Created: README.txt in bin/")


def main():
    print("开始构建...")

    print("清理旧构建...")
    clean_build()

    print("构建可执行文件...")
    build_exe()

    print("复制文档文件...")
    copy_docs()

    print(f"\n构建完成! 输出目录: {DIST_DIR}")
    print(f"可执行文件: {BIN_DIR}")


if __name__ == "__main__":
    main()
