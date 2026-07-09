# my-stock-portfolio-skill

基于 SQLite 的个人股票投资组合管理工具，提供命令行界面管理股票持仓、关注列表、交易记录和账户资金，可供openclaw等各种智能体直接调用。

为什么要单独做个skill呢，因为openclaw这种智能体太能干，有时候会绕过你写的脚本，直接操作你的SQLite。所以封装一下，只暴漏cli是个不错的方法

## 项目简介

这是一个用于管理个人股票投资组合的 CLI 工具，主要功能包括：

- **账户管理**：初始化账户、入金、出金、查看账户概览
- **持仓管理**：添加/更新/删除持仓、查看持仓列表
- **交易记录**：查询历史交易记录
- **关注列表**：管理关注的股票
- **数据持久化**：使用 SQLite 存储数据

## 技术栈

- Python 3.8+
- Typer（CLI 框架）
- SQLAlchemy（ORM）
- Pydantic（数据验证）
- PyInstaller（打包工具）

---

## 目录结构

```
my-stock-portfolio-skill/
├── CLAUDE.md                    # 项目开发规范
├── README.md                    # 本文件
├── requirements.txt             # 运行依赖
├── requirements-build.txt       # 打包依赖
├── build.py                     # 打包脚本
├── pytest.ini                   # pytest 配置
├── src/                         # 源代码目录
│   ├── __init__.py
│   ├── __main__.py              # CLI 入口
│   ├── config.py                # 配置管理
│   ├── cli/                     # CLI 命令模块
│   │   ├── position.py          # 持仓相关命令
│   │   ├── watch.py             # 关注列表命令
│   │   ├── transaction.py       # 交易记录命令
│   │   ├── account.py           # 账户管理命令
│   │   └── config.py            # 配置查看命令
│   ├── services/                # 业务逻辑层
│   │   ├── position_service.py
│   │   ├── watchlist_service.py
│   │   ├── transaction_service.py
│   │   └── account_service.py
│   ├── models/                  # 数据模型
│   │   └── schemas.py           # Pydantic 模型
│   ├── database/                # 数据库相关
│   │   ├── connection.py        # 数据库连接
│   │   └── models.py            # SQLAlchemy 模型
│   └── utils/                   # 工具函数
│       └── helpers.py
├── tests/                       # 测试目录
│   ├── conftest.py              # pytest fixtures
│   ├── test_services/           # 业务逻辑测试
│   ├── test_demo.py             # 功能演示脚本
│   └── simple_test.py           # 简单测试
├── data/                        # 数据目录（数据库文件）
├── dist/                        # 打包输出目录
│   ├── bin/                     # 可执行文件
│   ├── SKILL.md                 # Skill 使用说明
│   └── stock_portfolio_config.json.example  # 配置示例
└── docs/                        # 项目文档
    ├── 需求文档.md
    ├── 实现步骤.md
    └── output/                  # 输出文档
```

---

## 快速开始

### 方式一：使用 Release 下载包（推荐普通用户）

1. 从 [Releases](../../releases) 页面下载最新版本压缩包
2. 解压到任意目录
3. 参考目录下的 `README.txt` 配置数据库路径（可选）
4. 运行 `bin/my-stock-portfolio-cli` 开始使用

### 方式二：从源码编译使用

#### 1. 环境要求

- Python 3.8+
- pip

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 开发运行

```bash
# 直接运行 CLI
python -m src

# 查看帮助
python -m src --help
```

#### 4. 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行所有测试
python -m pytest

# 运行功能演示
python tests/test_demo.py
```

#### 5. 打包

```bash
# 安装打包依赖
pip install -r requirements-build.txt

# 执行打包
python build.py
```

打包完成后，可执行文件位于 `dist/bin/` 目录。

---

## 使用说明

### 基本命令格式

```
my-stock-portfolio-cli <command> <subcommand> [options]
```

### 可用命令

| 命令组 | 描述 |
|--------|------|
| account | 账户管理 |
| position | 持仓管理 |
| transaction | 交易记录查询 |
| watch | 关注列表管理 |
| config | 配置查看 |

### 使用示例

```bash
# 1. 初始化账户
my-stock-portfolio-cli account init --name "我的股票账户" --balance 100000

# 2. 买入股票
my-stock-portfolio-cli position add --code 600519 --name "贵州茅台" --quantity 100 --price 150.0

# 3. 查看持仓
my-stock-portfolio-cli position list

# 4. 查看账户概览
my-stock-portfolio-cli account info

# 5. 添加关注
my-stock-portfolio-cli watch add --code 000001 --name "平安银行"

# 6. 查看交易记录
my-stock-portfolio-cli transaction list
```

更多详细命令说明请参考 [dist/SKILL.md](dist/SKILL.md)（打包后）或 [docs/output/SKILL.md](docs/output/SKILL.md)（源码）。

---

## 配置说明

配置文件名为 `stock_portfolio_config.json`，需与可执行文件放在同一目录下。

### 配置文件格式

```json
{
    "db_path": "portfolio.db"
}
```

### db_path 配置规则

- **不配置**（默认）：
  - 开发阶段：`data/portfolio.db`
  - 打包后：`~/.stock_portfolio/portfolio.db`

- **配置为文件路径**：直接使用该文件
- **配置为目录路径**：在该目录下创建 `portfolio.db`
- 支持相对路径和绝对路径

查看当前配置：
```bash
my-stock-portfolio-cli config show
```

---

## 开发说明

### 项目架构

- **src/cli/**: Typer 命令定义，只负责参数解析和调用 service
- **src/services/**: 业务逻辑实现，包含核心功能
- **src/database/**: SQLAlchemy ORM 模型和数据库连接
- **src/models/**: Pydantic 数据验证模型
- **src/config.py**: 配置文件管理

### 添加新功能

1. 在 `src/services/` 中添加业务逻辑
2. 在 `src/cli/` 中添加对应的 CLI 命令
3. 在 `tests/test_services/` 中添加测试

### 代码规范

- 所有测试文件放在 `tests/` 目录下
- 使用 `python -m pytest` 运行测试
- 提交前确保测试通过

---

## License

MIT
