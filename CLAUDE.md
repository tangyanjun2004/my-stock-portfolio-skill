# 我的股票投资组合 Skill

这是一个用于管理持仓股票和关注股票的 Claude Code Skill，提供统一的 CLI 命令供 OpenClaw 使用。

## 项目描述

- **技术栈**: Python 3.8+
- **数据存储**: SQLite
- **主要功能**: 股票持仓管理、关注列表管理、交易记录查询、账户查询、配置查看、统一 CLI 接口
- **打包工具**: PyInstaller
- **测试框架**: pytest

## 项目结构

```
my-stock-portfolio-skill/
├── CLAUDE.md                    # 项目文档
├── requirements.txt            # 依赖清单
├── requirements-build.txt      # 打包依赖
├── README.md                   # 使用说明
├── build.py                    # 打包脚本
├── pytest.ini                  # pytest 配置
├── src/                        # 主源码目录
│   ├── __init__.py
│   ├── __main__.py             # CLI 入口
│   ├── config.py               # 配置管理
│   ├── cli/                    # CLI 命令模块
│   │   ├── __init__.py
│   │   ├── position.py         # 持仓相关命令
│   │   ├── watch.py            # 关注列表相关命令
│   │   ├── transaction.py      # 交易记录相关命令
│   │   ├── account.py          # 账户相关命令
│   │   └── config.py           # 配置查看命令
│   ├── services/               # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── position_service.py
│   │   ├── watchlist_service.py
│   │   ├── transaction_service.py
│   │   └── account_service.py
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic 模型
│   ├── database/               # 数据库相关
│   │   ├── __init__.py
│   │   ├── connection.py       # 数据库连接
│   │   └── models.py           # SQLAlchemy 模型
│   └── utils/                  # 工具函数
│       ├── __init__.py
│       └── helpers.py
├── tests/                      # 测试目录（所有测试文件必须放在这里）
│   ├── __init__.py
│   ├── conftest.py             # pytest fixtures
│   ├── test_services/          # 业务逻辑测试
│   ├── test_demo.py            # 功能演示脚本
│   └── simple_test.py          # 简单测试脚本
├── test-results/               # 测试结果输出目录
├── data/                       # 数据目录
├── dist/                       # 打包输出目录
│   ├── bin/                    # 可执行文件目录
│   ├── SKILL.md                # Skill 详细使用说明
│   ├── stock_portfolio_config.json.example  # 配置文件示例
│   └── CONFIG_README.txt       # 配置说明
└── docs/                       # 文档目录
    ├── 需求文档.md
    ├── 实现步骤.md
    └── output/                 # 输出文档目录
        ├── SKILL.md            # Skill 使用说明（源文件）
        └── stock_portfolio_config.json.example  # 配置文件示例（源文件）
```

## 目录放置规范

| 目录/文件 | 说明 |
|-----------|------|
| `src/cli/` | CLI 命令定义，使用 Typer 框架 |
| `src/services/` | 业务逻辑实现，处理核心功能 |
| `src/models/` | Pydantic 数据验证模型 |
| `src/database/` | SQLAlchemy ORM 模型和数据库连接 |
| `src/config.py` | 配置文件管理 |
| `tests/` | 测试代码目录（所有测试文件必须放在这里） |
| `test-results/` | 测试结果输出目录（覆盖率报告等） |
| `data/` | SQLite 数据库文件存储位置 |
| `dist/bin/` | 打包后的 exe 文件 |
| `docs/` | 项目文档 |
| `docs/output/` | 输出文档目录（SKILL.md 等） |

## 配置文件

配置文件名为 `stock_portfolio_config.json`，需与可执行文件放在同一目录下。

### 配置文件格式

```json
{
    "db_path": "portfolio.db"
}
```

### db_path 配置规则

- 如果不配置，使用默认路径：
  - 开发阶段：项目目录下的 `data/portfolio.db`
  - 打包后：用户目录下的 `.stock_portfolio/portfolio.db`

- 如果配置为文件路径，直接使用该文件
- 如果配置为目录路径，会在该目录下创建 `portfolio.db`
- 支持相对路径和绝对路径

**注意**：配置文件需要手动创建和编辑，不提供 CLI 命令进行配置修改。

## 开发命令

- `python -m src` - 运行 CLI（开发阶段）
- `python tests/test_demo.py` - 运行功能演示
- `python -m pytest` - 运行测试
- `python build.py` - 打包成 exe

## 最终交付物

```
dist/
├── SKILL.md                            # Skill 详细使用说明
├── stock_portfolio_config.json.example  # 配置文件示例
├── CONFIG_README.txt                   # 配置说明
└── bin/
    ├── my-stock-portfolio-cli.exe      # Windows 可执行文件
    └── my-stock-portfolio-cli          # Linux 可执行文件
```

## 注意事项

- 数据库文件默认位于 `data/portfolio.db`，需要确保有写入权限
- 打包后的 exe 默认将数据库放在用户目录下的 `.stock_portfolio` 文件夹中
- 可以通过配置文件 `stock_portfolio_config.json` 自定义数据库路径
- 配置文件需要手动编辑，不提供 CLI 配置修改命令
- `test-results/` 目录中的内容不会提交到版本控制
- **所有测试文件必须放在 tests 目录下**，包括演示脚本和临时测试脚本
