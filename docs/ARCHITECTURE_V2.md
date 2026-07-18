# V2 系统架构文档 — Core Engineering

## 1. 版本定位

V2 ≠ 加功能。V2 = 打地基。

V1 证明了业务逻辑可行（Pipeline 跑通了）。但工程基础薄弱：
硬编码路径、`print()` 散落各处、无类型检查、无测试、无分层。

V2 的目标是让项目从"能跑的脚本"升级为"可维护的软件"。

V2 不引入 Streamlit，不新增任何业务模块，只做工程化改造。

## 2. 目标架构：四层分层模型

这是 V2 的**目标架构** —— Sprint 2.1 不会一次性建完，但所有 V2 的 Story 都服务于这个最终形态。

```
┌──────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  负责：接收用户输入，展示结果                                   │
│                                                              │
│  V1: main.py (CLI)                                           │
│  V3: app.py (Streamlit)                                      │
│  V7: API routes (FastAPI, 未来)                               │
│                                                               │
│  规则：Presentation 层不包含任何业务逻辑。                      │
│        只调用 Service Layer，不直接访问 Data/Business 层。      │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                      Service Layer                           │
│  负责：流程编排、横切关注点（日志、配置、错误处理）               │
│                                                               │  
│  src/pipeline_service.py   —— 编排 Load → Clean → Analyze    │
│  src/config.py             —— 集中配置管理                    │
│  src/logger.py             —— 结构化日志                       │
│  src/exceptions.py         —— 自定义异常体系                    │
│                                                              │
│  规则：Service 层调用 Business 层，不直接读文件或操作 DataFrame。 │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                      Business Layer                           │
│  负责：业务计算逻辑，纯数据变换                                    │
│                                                              │
│  src/sales_analyzer.py     —— 销售 KPI 计算                   │
│  src/customer_analyzer.py  —— RFM 客户分层                    │
│  src/visualizer.py         —— 图表生成                        │
│  src/report_generator.py   —— HTML 报告组装                   │
│                                                              │
│  规则：函数签名 (DataFrame | dict) → dict。                      │
│        不读文件，不写文件，不 print，不处理异常（交给 Service 层）。  │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                       Data Layer                              │
│  负责：数据存取，外部 I/O                                        │
│                                                              │
│  src/data_loader.py        —— CSV → DataFrame                 │
│  src/data_cleaner.py       —— 数据清洗                         │
│                                                              │
│  规则：这是唯一可以读写文件的层。                                  │
│        V6 引入 Database 后，这层增加 SQL 查询替代 CSV 读取。       │
└──────────────────────────────────────────────────────────────┘
```

### 2.1 层间调用规则

```
Presentation ──→ Service ──→ Business ──→ Data
     │                            │
     ├── 不可直接调用 ────────────┤
     ├── 不可直接调用 ──────────────────────┤
     │
     Service ──→ 不可直接调用 ──→ Data（通过 Business 层中转）
```

**硬约束：**
- 上层可以调用紧邻下层，不能跨层调用
- 下层绝不知道上层的存在（Data 层不 import Service 层）
- 同层模块之间可以通过 dict 传递数据，但不能相互 import（Business 之间独立）

### 2.2 V1 现状 vs V2 目标

| 模块 | V1 所在层（隐式） | V2 归属层 | V2 改动 |
|------|------------------|----------|---------|
| `main.py` | Presentation | Presentation | 精简为薄壳，逻辑移入 PipelineService |
| `data_loader.py` | Data | Data | 加 type hints + logger + 自定义异常 |
| `data_cleaner.py` | Data | Data | 加 type hints + logger + 自定义异常 |
| `data_profiler.py` | Data/Business | Data | 加 type hints + logger |
| `sales_analyzer.py` | Business | Business | 加 type hints + 移除 print |
| `customer_analyzer.py` | Business | Business | 加 type hints + 移除 print |
| `visualizer.py` | Business | Business | 加 type hints + 移除 print |
| `report_generator.py` | Business | Business | 加 type hints + 移除 print |
| — | — | Service | **新增**：pipeline_service, config, logger, exceptions |

## 3. V2 核心模块设计

### 3.1 Config System（`src/config.py`）

详见 [docs/CONFIG_DESIGN.md](CONFIG_DESIGN.md)。

```
load_config(path) → dict
       │
       ├─ YAML 存在 → 解析 → 校验 → 返回 dict
       └─ YAML 缺失 → 打印警告 → 返回内置默认值
```

### 3.2 Logging System（`src/logger.py`）

```
setup_logging(config: dict) → None
       │
       ├─ 读取 config["logging"]["level"]
       ├─ 配置 root logger：控制台 handler + 文件 handler
       └─ 文件输出：logs/app.log
```

**日志级别使用约定：**
| 级别 | 使用场景 |
|------|---------|
| DEBUG | 变量值、中间计算结果（仅开发时开启） |
| INFO | 关键步骤完成（"数据加载成功，541,910 行"） |
| WARNING | 可恢复的异常（"缺失值 5%，已自动填充"） |
| ERROR | 不可恢复但可捕获（"文件不存在，流程终止"） |

**关键规则：** `src/` 模块内部不使用 `print()`。模块通过 logger 输出信息，由 Presentation 层决定如何展示。

唯一的例外：`data_profiler.py` 的职责就是打印数据报告，V2 中保留其 `print()` 但标记为 tech debt。

### 3.3 Exception Hierarchy（`src/exceptions.py`）

```
CrossBorderDashboardError (基类)
├── ConfigError              —— 配置加载/校验失败
├── DataLoadError            —— 文件读取失败
├── DataCleanError           —— 清洗过程异常（空 DataFrame 等）
└── AnalysisError            —— 分析计算异常
```

**使用规则：**
- 只在 Data 层和 Service 层 raise 异常
- Business 层不捕获也不抛出异常 — 假设输入合法
- Presentation 层负责 try/except 并展示用户友好信息

### 3.4 PipelineService（`src/pipeline_service.py`）

这是 V2 的核心新增模块，承担当前 `main.py` 中的编排逻辑：

```python
class PipelineService:
    """
    编排完整的数据分析流程。

    用法:
        service = PipelineService(config)
        result = service.run(data_path="data/raw/sales.csv")
        # result = {"sales": {...}, "customers": {...}, "charts": [...]}
    """

    def __init__(self, config: dict):
        self.config = config

    def run(self, data_path: str | None = None) -> dict:
        """执行全流程：加载 → 诊断 → 清洗 → 分析 → 可视化 → 报告。"""
        ...
```

**为什么用 Class 而不是 Function：**
- 需要持有 config 引用（多个方法共用，避免传参）
- V3 中 Streamlit 可以通过同一 Service 实例调用单个步骤（而非每次跑全流程）
- V7 中 API 可以通过 DI 注入 Service

### 3.5 V2 目标目录结构

```
cross-border-dashboard/
├── config.yaml                   # 全局配置（V2 新增）
├── mypy.ini                      # mypy 配置（V2 新增）
├── main.py                       # V1 CLI 入口（V2 重构）
├── requirements.txt
│
├── src/
│   │
│   ├── config.py                 # Service Layer — 配置加载（V2 新增）
│   ├── logger.py                 # Service Layer — 日志初始化（V2 新增）
│   ├── exceptions.py             # Service Layer — 自定义异常（V2 新增）
│   ├── pipeline_service.py       # Service Layer — 流程编排（V2 新增）
│   │
│   ├── data_loader.py            # Data Layer（V2 重构：+type hints, +logger）
│   ├── data_cleaner.py           # Data Layer（V2 重构）
│   ├── data_profiler.py          # Data Layer（V2 重构）
│   │
│   ├── sales_analyzer.py         # Business Layer（V2 重构）
│   ├── customer_analyzer.py      # Business Layer（V2 重构）
│   ├── visualizer.py             # Business Layer（V2 重构）
│   └── report_generator.py       # Business Layer（V2 重构）
│
├── tests/                        # V2 新增
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_sales_analyzer.py
│   └── test_customer_analyzer.py
│
├── logs/                         # V2 新增（git-ignored）
│   └── app.log
│
├── docs/
│   ├── ARCHITECTURE.md           # V1 架构（冻结，历史参考）
│   ├── ARCHITECTURE_V2.md        # V2+ 架构（本文档）
│   ├── DEVELOPMENT.md
│   └── CONFIG_DESIGN.md
│
├── data/
│   ├── raw/
│   └── processed/
└── output/
    ├── charts/
    └── reports/
```

**V2 目录变化摘要：**
- `src/` 平铺 → 保持平铺（V2 暂不分子目录，< 15 文件不需要）
- 新增 4 个 Service Layer 模块：config, logger, exceptions, pipeline_service
- 新增 `tests/` 目录
- 新增 `logs/` 目录
- `docs/` 新增 ARCHITECTURE_V2.md, CONFIG_DESIGN.md

## 4. 设计原则

这些原则适用于 V2 及之后所有版本。

### 4.1 Architecture First

> 架构设计先于代码实现。

- 任何新模块必须先有架构文档说明它在四层模型中的位置、输入/输出、依赖
- Sprint 开始前，所有 Story 的 AC 必须完整
- 不允许"先写了再补文档"

### 4.2 Single Responsibility Principle

> 一个模块只做一件事，只因为一个原因变化。

- Data 层模块负责 I/O
- Business 层模块负责纯计算
- Service 层模块负责编排
- Presentation 层模块负责用户交互

### 4.3 Low Coupling, High Cohesion

> 模块之间通过 dict 传递数据，不共享状态。

- 模块之间的依赖关系必须是单向的（上层依赖下层）
- 同层模块之间不相互 import
- 数据流遵循 Pipeline First 模式

### 4.4 Pipeline First

> 数据从进入系统到输出结果，流经的每一步都是可预测、可测试的。

- 每个模块的输入和输出类型在函数签名中声明
- Pipeline 的每个阶段互不干扰，可以独立替换

### 4.5 Review Before Merge

> 所有代码变更在合入 main 之前必须通过 Code Review。

- 单人项目 = 自审（对照 DEVELOPMENT.md 的 Code Review Checklist）
- 如有外部贡献者 = PR review

### 4.6 Documentation First

> 文档是交付物的一部分，不是事后补充。

- 新模块 = 架构文档 + docstring
- Story 完成 = AC 全部打勾 + commit message 清晰

## 5. V3-V7 扩展路径

V2 的分层架构为后续版本预留了明确的扩展点：

```
V3 — Streamlit Dashboard
    └── 在 Presentation 层新增 app.py + src/ui/
        复用 V2 的 Service → Business → Data 全部三层

V4 — Interactive Analytics
    └── 替换 Business 层的 visualizer.py（Matplotlib → Plotly）
        Presentation 层新增交互组件

V5 — AI Report
    └── Business 层新增 ai_analyzer.py
        Service 层新增 AI client 管理
        Config 层新增 api keys 配置

V6 — Database Integration
    └── Data 层新增 database_loader.py（替代 csv_loader）
        Business 层和 Service 层无需改动

V7 — Deployment
    └── 跨层关注：Dockerfile, CI/CD, Cloud config
        代码架构不变
```

## 6. V1 冻结声明

V1（`docs/ARCHITECTURE.md` 描述的 Pipeline）已冻结。

- ✅ 所有 V1 模块功能稳定
- ✅ V2 只重构代码质量（type hints, logging, exceptions），不改变业务逻辑
- ✅ 如果 V2 重构引入 bug，V1 的 11 个 commit 是回退锚点
- ❌ V1 不接受新功能需求
