---
name: my-stocks-portfolio
description: 个人股票数据库管理 - 基于SQLite封装个人持仓/关注/账户信息，提供命令行工具管理持仓、交易、个人关注的和账户数据。
version: 0.1.0
---

# 股票投资组合管理 Skill 使用说明

## 概述

这是一个用于管理股票持仓和关注列表的 Claude Code Skill，提供统一的 CLI 命令供 OpenClaw 使用。

## 什么时候使用

当你需要进行以下操作时使用此 Skill：

- 管理股票账户（初始化、入金、出金、查看账户概览）
- 管理股票持仓（添加、更新、删除、查看持仓）
- 管理股票关注列表（添加、删除、查看关注）
- 查询交易历史记录

## 如何使用

### 进入脚本目录

```bash
cd {baseDir}/bin
```

### 基本调用格式

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

### 全局选项

| 选项 | 描述 |
|------|------|
| --version, -v | 显示版本号 |
| --help | 显示帮助信息 |

---

## 命令详解

### 1. account - 账户管理

#### 1.1 init - 初始化账户

**功能**：创建一个新的股票投资账户

**使用方式**：
```
my-stock-portfolio-cli account init --name <账户名称> --balance <初始金额>
```

**入参**：
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| --name | string | 是 | 账户名称 |
| --balance | float | 是 | 初始资金金额 |

**示例**：
```
my-stock-portfolio-cli account init --name "我的股票账户" --balance 100000
```

**出参**：
- 成功：显示账户创建成功信息
- 失败：显示错误信息（如账户已存在）

---

#### 1.2 info - 查看账户概览

**功能**：查看当前账户的详细信息

**使用方式**：
```
my-stock-portfolio-cli account info
```

**入参**：无

**出参**：
显示账户概览信息，包括：
- 账户名称
- 总资产
- 可用余额
- 持仓市值
- 总投入
- 持仓数量

---

#### 1.3 deposit - 入金

**功能**：向账户转入资金

**使用方式**：
```
my-stock-portfolio-cli account deposit <金额> [--note <备注>]
```

**入参**：
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| 金额 | float | 是 | 转入金额 |
| --note | string | 否 | 备注信息 |

**示例**：
```
my-stock-portfolio-cli account deposit 50000 --note "追加投资"
```

**出参**：
- 成功：显示入金成功信息
- 失败：显示错误信息

---

#### 1.4 withdraw - 出金

**功能**：从账户转出资金

**使用方式**：
```
my-stock-portfolio-cli account withdraw <金额> [--note <备注>]
```

**入参**：
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| 金额 | float | 是 | 转出金额 |
| --note | string | 否 | 备注信息 |

**示例**：
```
my-stock-portfolio-cli account withdraw 10000 --note "取出收益"
```

**出参**：
- 成功：显示出金成功信息
- 失败：显示错误信息（如余额不足）

---

### 2. position - 持仓管理

#### 2.1 add - 添加持仓

**功能**：买入股票，添加新的持仓记录

**使用方式**：
```
my-stock-portfolio-cli position add --code <股票代码> --name <股票名称> --quantity <数量> --price <价格> [--date <日期>]
```

**入参**：
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| --code | string | 是 | 股票代码（如 600519） |
| --name | string | 是 | 股票名称（如 贵州茅台） |
| --quantity | float | 是 | 买入数量 |
| --price | float | 是 | 买入价格 |
| --date | string | 否 | 买入日期（格式：YYYY-MM-DD，默认为今天） |

**示例**：
```
my-stock-portfolio-cli position add --code 600519 --name "贵州茅台" --quantity 100 --price 150.0 --date 2024-01-15
```

**出参**：
- 成功：显示持仓添加成功信息
- 失败：显示错误信息（如余额不足、持仓已存在）

---

#### 2.2 list - 查看持仓列表

**功能**：查看所有持仓股票

**使用方式**：
```
my-stock-portfolio-cli position list
```

**入参**：无

**出参**：
显示所有持仓列表，包括：
- 股票代码
- 股票名称
- 持仓数量
- 平均成本
- 当前市值（按成本计算）

---

#### 2.3 show - 查看单个持仓详情

**功能**：查看某支股票的详细持仓信息

**使用方式**：
```
my-stock-portfolio-cli position show <股票代码或持仓ID>
```

**入参**：
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| 股票代码或ID | string/int | 是 | 股票代码或持仓ID |

**示例**：
```
my-stock-portfolio-cli position show 600519
```

**出参**：
显示持仓详细信息，包括：
- 股票代码和名称
- 持仓数量
- 平均成本
- 总投入
- 创建和更新时间

---

#### 2.4 update - 更新持仓（买入/卖出）

**功能**：对已有持仓进行买入或卖出操作

**使用方式**：
```
my-stock-portfolio-cli position update <股票代码或持仓ID> --type <buy|sell> --quantity <数量> --price <价格> [--date <日期>]
```

**入参**：
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| 股票代码或ID | string/int | 是 | 股票代码或持仓ID |
| --type | string | 是 | 操作类型：buy（买入）或 sell（卖出） |
| --quantity | float | 是 | 交易数量 |
| --price | float | 是 | 交易价格 |
| --date | string | 否 | 交易日期（格式：YYYY-MM-DD，默认为今天） |

**示例**：
```
# 加仓
my-stock-portfolio-cli position update 600519 --type buy --quantity 50 --price 160.0

# 减仓
my-stock-portfolio-cli position update 600519 --type sell --quantity 30 --price 165.0
```

**出参**：
- 成功：显示持仓更新成功信息
- 失败：显示错误信息（如持仓不存在、余额不足、持仓数量不足）

---

#### 2.5 remove - 删除持仓

**功能**：删除某支股票的持仓记录（将持仓数量算作卖出，资金返回可用余额）

**使用方式**：
```
my-stock-portfolio-cli position remove <股票代码或持仓ID>
```

**入参**：
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| 股票代码或ID | string/int | 是 | 股票代码或持仓ID |

**示例**：
```
my-stock-portfolio-cli position remove 600519
```

**出参**：
- 成功：显示持仓删除成功信息
- 失败：显示错误信息（如持仓不存在）

---

### 3. transaction - 交易记录查询

#### 3.1 list - 查看交易记录

**功能**：查询历史交易记录

**使用方式**：
```
my-stock-portfolio-cli transaction list [--stock <股票代码>] [--start <开始日期>] [--end <结束日期>]
```

**入参**：
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| --stock | string | 否 | 按股票代码筛选 |
| --start | string | 否 | 开始日期（格式：YYYY-MM-DD） |
| --end | string | 否 | 结束日期（格式：YYYY-MM-DD） |

**示例**：
```
# 查看所有交易
my-stock-portfolio-cli transaction list

# 查看某支股票的交易
my-stock-portfolio-cli transaction list --stock 600519

# 查看某时间段的交易
my-stock-portfolio-cli transaction list --start 2024-01-01 --end 2024-06-30
```

**出参**：
显示符合条件的交易记录列表，包括：
- 交易类型（买入/卖出）
- 股票代码和名称
- 交易数量
- 交易价格
- 交易金额
- 交易日期

---

### 4. watch - 关注列表管理

#### 4.1 add - 添加关注

**功能**：将股票添加到关注列表

**使用方式**：
```
my-stock-portfolio-cli watch add --code <股票代码> --name <股票名称> [--note <备注>]
```

**入参**：
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| --code | string | 是 | 股票代码 |
| --name | string | 是 | 股票名称 |
| --note | string | 否 | 备注信息 |

**示例**：
```
my-stock-portfolio-cli watch add --code AAPL --name "苹果公司" --note "关注中"
```

**出参**：
- 成功：显示关注添加成功信息
- 失败：显示错误信息（如已在关注列表中）

---

#### 4.2 list - 查看关注列表

**功能**：查看所有关注的股票

**使用方式**：
```
my-stock-portfolio-cli watch list
```

**入参**：无

**出参**：
显示关注列表，包括：
- 股票代码
- 股票名称
- 备注
- 添加时间

---

#### 4.3 remove - 移除关注

**功能**：从关注列表中移除某支股票

**使用方式**：
```
my-stock-portfolio-cli watch remove <股票代码或关注ID>
```

**入参**：
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| 股票代码或ID | string/int | 是 | 股票代码或关注ID |

**示例**：
```
my-stock-portfolio-cli watch remove AAPL
```

**出参**：
- 成功：显示关注移除成功信息
- 失败：显示错误信息（如未找到关注项）

---

### 5. config - 配置查看

#### 5.1 show - 查看当前配置

**功能**：显示当前的配置信息

**使用方式**：
```
my-stock-portfolio-cli config show
```

**入参**：无

**出参**：
显示配置信息，包括：
- 配置文件路径
- 配置文件是否存在
- 数据库路径配置
- 实际数据库位置

---

## 使用流程示例

### 完整的使用流程

1. **初始化账户**
   ```
   my-stock-portfolio-cli account init --name "我的投资账户" --balance 100000
   ```

2. **添加持仓**
   ```
   my-stock-portfolio-cli position add --code 600519 --name "贵州茅台" --quantity 100 --price 150.0
   ```

3. **添加关注**
   ```
   my-stock-portfolio-cli watch add --code 000001 --name "平安银行" --note "观察"
   ```

4. **查看账户概览**
   ```
   my-stock-portfolio-cli account info
   ```

5. **查看持仓列表**
   ```
   my-stock-portfolio-cli position list
   ```

6. **加仓操作**
   ```
   my-stock-portfolio-cli position update 600519 --type buy --quantity 50 --price 160.0
   ```

7. **查看交易记录**
   ```
   my-stock-portfolio-cli transaction list
   ```

---

## 注意事项

1. **账户初始化**：首次使用必须先初始化账户
2. **资金充足性**：买入股票前需要确保可用余额充足
3. **持仓数量**：卖出股票时不能超过当前持仓数量
4. **数据备份**：建议定期备份数据库文件
5. **配置修改**：配置文件需要手动编辑，没有提供 CLI 修改命令

---

## 版本信息

当前版本：v0.1.0

查看版本：
```
my-stock-portfolio-cli --version
```
