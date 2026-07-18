# 项目路线图

## 版本演进

```
V1  ✅  Local Analytics      ──  Python CLI, Pandas, Matplotlib
V2  🚧  Core Engineering      ──  工程化基础（当前）
V3  🚧  Streamlit Dashboard   ──  Web 互动看板
V4  🚧  Interactive Analytics ──  Plotly 动态图表
V5  🚧  AI Report             ──  LLM 智能分析报告
V6  🚧  Database Integration  ──  数据持久化
V7  🚧  Deployment            ──  Docker, CI/CD, Cloud
```

---

## V1.0 — Local Analytics ✅ DONE（已冻结）

**目标**：完成完整的数据分析管道。`python main.py` 一键运行，
输出终端报告 + HTML 报告 + 图表文件。

**技术栈**：Python, Pandas, NumPy, Matplotlib

**版本状态**：🔒 Version Freeze — 除 Bug Fix 外不再新增功能。

### Stories

| Story | 模块 | 交付物 | 状态 |
|-------|--------|------------|------|
| S1.1 | DataProfiler | 数据质量诊断报告（终端输出） | ✅ |
| S1.2 | DataCleaner | `data/processed/sales_clean.csv`（541,910 → 392,693 行） | ✅ |
| S1.3 | SalesAnalyzer | 销售 KPI（总营收 $8.89M、18.5K 订单） | ✅ |
| S1.4 | CustomerAnalyzer | RFM 客户分层（4,338 客户、三层分级） | ✅ |
| S1.5 | Visualizer | 8 张 Matplotlib 图表 → `output/charts/` | ✅ |
| S1.6 | ReportGenerator | 自包含 HTML 报告 → `output/reports/report.html` | ✅ |

**V1 成果**：7 个 src 模块、11 个 commit、一键运行完整分析。

---

## V2.0 — Core Engineering 🚧 进行中

**目标**：建立可持续迭代的软件工程基础。不新增业务功能，
专注于代码质量、可维护性和工程基础设施。

**技术栈新增**：PyYAML, pytest, mypy

**核心理念**：V2 不是加功能，是打地基。所有后续版本（V3-V7）建立在 V2 的工程基础之上。

---

### Sprint 2.1 — Engineering Foundation（当前）

**Sprint 目标**：Config System, Logging, Type Hints, Exception Handling 四大基础设施就位。

---

#### Story 2.1.1 — Config System

> As a developer, I want a centralized YAML configuration so that all paths
> and parameters are managed in one place instead of scattered through code.

**设计文档**：[docs/CONFIG_DESIGN.md](docs/CONFIG_DESIGN.md)

**Tasks:**

- [ ] **Task 1** — 实现 `src/config.py`：`load_config()` 解析 YAML + schema 校验 + 默认值降级
- [ ] **Task 2** — 创建 `config.yaml`：按 CONFIG_DESIGN.md 的 5 域 20 字段 schema
- [ ] **Task 3** — 重构 `main.py`：所有硬编码路径替换为 config 取值
- [ ] **Task 4** — 编写 `tests/test_config.py`：正常加载 / 文件缺失降级 / 字段缺失报错

**Acceptance Criteria:**

- [ ] **AC1** — `load_config()` 返回完整 dict，所有字段可索引取值
- [ ] **AC2** — `config.yaml` 缺失时打印警告并返回内置默认值（不崩溃）
- [ ] **AC3** — 必填字段缺失时抛出明确错误信息（不静默降级）
- [ ] **AC4** — `main.py` 中零硬编码路径
- [ ] **AC5** — `pytest tests/test_config.py` 3 个场景全部通过

---

#### Story 2.1.2 — Logging System

> As a developer, I want structured logging with configurable levels so that
> I can debug issues without relying on scattered print() statements.

**Tasks:**

- [ ] **Task 1** — 实现 `src/logger.py`：基于标准库 `logging`，支持控制台 + 文件双输出
- [ ] **Task 2** — 将所有 `src/` 模块中的 `print()` 替换为 `logger.info()` / `logger.warning()` / `logger.error()`
- [ ] **Task 3** — 日志级别由 `config.yaml` 控制（默认 INFO）
- [ ] **Task 4** — `main.py` 启动时调用 `setup_logging(config)` 初始化

**Acceptance Criteria:**

- [ ] **AC1** — `python main.py` 运行时终端输出格式：`2026-07-18 14:30:00 [INFO] src.data_loader: 数据读取成功`
- [ ] **AC2** — 日志同时写入 `logs/app.log` 文件
- [ ] **AC3** — 修改 `config.yaml` 中 log level 为 `DEBUG` 后，重启可看到更详细的日志
- [ ] **AC4** — `src/` 目录下零 `print()` 调用（`data_profiler.py` 除外 — 其职责是终端报告）
- [ ] **AC5** — 异常信息通过 `logger.exception()` 输出完整 traceback

---

#### Story 2.1.3 — Type Hints

> As a developer, I want complete type annotations on all function signatures
> so that my IDE provides accurate autocomplete and mypy catches type errors.

**Tasks:**

- [ ] **Task 1** — 为所有 7 个 V1 模块的函数签名添加完整 type hints
- [ ] **Task 2** — 添加 `mypy.ini` 配置文件（strict mode for V2+ modules）
- [ ] **Task 3** — 运行 `mypy src/` 并修复所有类型错误
- [ ] **Task 4** — 更新 DEVELOPMENT.md 的 §2.3：Type Hints 从 "Recommended" 改为 "Required"

**Acceptance Criteria:**

- [ ] **AC1** — `src/` 下所有公共函数签名包含参数类型和返回类型
- [ ] **AC2** — `mypy src/ --strict` 零错误
- [ ] **AC3** — 使用 `dict[str, Any]` 作为分析结果 dict 的返回类型（V2 暂不引入 TypedDict）

---

#### Story 2.1.4 — Exception Handling

> As a developer, I want graceful error handling with clear messages so that
> pipeline failures are debuggable instead of producing raw tracebacks.

**Tasks:**

- [ ] **Task 1** — 创建 `src/exceptions.py`：定义 `DataLoadError`, `DataCleanError`, `AnalysisError`, `ConfigError`
- [ ] **Task 2** — `data_loader.py` 中：文件不存在 → raise `DataLoadError`（而非 return None）
- [ ] **Task 3** — `main.py` 中：顶层 try/except 捕获所有自定义异常，打印用户友好信息后退出
- [ ] **Task 4** — `data_cleaner.py` 中：空 DataFrame → raise `DataCleanError`

**Acceptance Criteria:**

- [ ] **AC1** — 删除 `data/raw/sales.csv` 后运行 `python main.py`，输出清晰的错误信息（非 traceback 堆栈）
- [ ] **AC2** — 所有自定义异常继承自 `CrossBorderDashboardError`（基类）
- [ ] **AC3** — 每个异常类包含描述性 docstring
- [ ] **AC4** — V1 原有功能不受影响（正常路径行为不变）

---

### Sprint 2.2 — Service Layer + Testing（后续）

**Sprint 目标**：引入 Service Layer 解耦编排逻辑，建立完整的测试体系。

| Story | 描述 |
|-------|------|
| S2.2.1 — Service Layer | 实现 `src/pipeline_service.py` 编排全流程，`main.py` 退化为薄壳调用 |
| S2.2.2 — Testing Foundation | `tests/` 目录 + conftest.py + 所有 V1 模块的单元测试 |
| S2.2.3 — CLI 重构 | `main.py` 精简为：加载 config → setup logging → 调用 PipelineService |

---

### Sprint 2.3 — Directory Restructure + Code Quality（后续）

**Sprint 目标**：规范目录结构，代码质量全面达标。

| Story | 描述 |
|-------|------|
| S2.3.1 — Directory Restructure | 按分层架构重组 `src/` 子目录（data / business / service） |
| S2.3.2 — Remove Dead Code | 清理所有未使用的 import、注释掉的代码 |
| S2.3.3 — Docstring Audit | 确保所有公共函数有中文 docstring |

---

## V3.0 — Streamlit Dashboard 🚧 规划中

**目标**：将 V2 的业务模块对接到 Web 互动看板。

**技术栈新增**：Streamlit

**核心约束**：Streamlit 仅作为 Presentation Layer，所有业务逻辑调用 V2 的 Service Layer。

### Stories（概要）

| Story | 描述 |
|-------|------|
| S3.1 — App Shell | Streamlit 入口 + sidebar 四页导航 + 页面路由 |
| S3.2 — Overview Page | KPI 卡片 + 月度营收图 + Top 排名表 |
| S3.3 — Sales Page | 销售分析页：趋势图、商品排行、国家排行 |
| S3.4 — Customer Page | 客户分析页：RFM 分段、客户明细表 |
| S3.5 — Filters | 日期范围选择器、国家多选、Top N 滑块 |
| S3.6 — Data Upload | 用户上传自定义 CSV 文件 |

---

## V4.0 — Interactive Analytics 🚧 规划中

**目标**：用 Plotly 替换 Matplotlib，实现可交互的动态图表。

**技术栈新增**：Plotly

| Story | 描述 |
|-------|------|
| S4.1 — Plotly Migration | 8 张图表从 Matplotlib 迁移到 Plotly |
| S4.2 — Advanced Filters | 商品搜索、日期细粒度筛选 |
| S4.3 — Drill-down | 图表点击下钻到明细数据 |

---

## V5.0 — AI Report 🚧 规划中

**目标**：集成 LLM 生成叙述性分析报告。

**技术栈新增**：Anthropic API / OpenAI API

| Story | 描述 |
|-------|------|
| S5.1 — AI Summary | 从分析结果自动生成英文叙述性摘要 |
| S5.2 — Anomaly Detection | AI 标记数据中的异常模式 |
| S5.3 — NL Query | 自然语言输入 → 自动生成图表 |
| S5.4 — PDF Export | 精美排版的多页 PDF 报告 |

---

## V6.0 — Database Integration 🚧 规划中

**目标**：用数据库替代 CSV 文件，支持更大数据量和并发查询。

**技术栈新增**：SQLite（开发）/ PostgreSQL（生产）, SQLAlchemy

| Story | 描述 |
|-------|------|
| S6.1 — Schema Design | 数据库表结构设计 + 迁移脚本 |
| S6.2 — ETL Pipeline | CSV → DB 导入流程 |
| S6.3 — Query Layer | DataLoader 改为从 DB 查询 |

---

## V7.0 — Deployment 🚧 规划中

**目标**：容器化部署，支持云端访问。

**技术栈新增**：Docker, GitHub Actions, Cloud (TBD)

| Story | 描述 |
|-------|------|
| S7.1 — Docker | Dockerfile + docker-compose |
| S7.2 — CI/CD | GitHub Actions：lint → test → build |
| S7.3 — Cloud Deploy | 部署到云平台（Streamlit Cloud / VPS） |

---

## 版本原则

1. **V1 已冻结** — 除 Bug Fix 外不再新增功能。所有新能力从 V2 开始。
2. **文档先行** — 每个 Sprint 开始前，Architecture + Story + AC 必须已完成。
3. **Review Before Merge** — 所有代码合并前需通过 Code Review Checklist。
4. **Pipeline First** — 数据流设计先于代码实现。
5. **V2 是地基** — V3-V7 的所有 Presentation 层变更都不应触及 V2 的 Service/Business 层。
