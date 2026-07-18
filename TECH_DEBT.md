# Technical Debt & Future Roadmap

本文档记录项目中已知的技术债务和待实现功能。这些不是 Bug，而是有意识的推迟决策。

## Format

每条记录包含：优先级、标题、描述、预计版本。

优先级定义：
- **P0** — 影响代码可维护性，应在当前版本解决
- **P1** — 下一个版本应解决
- **P2** — 长期规划，有明确版本目标
- **P3** — 想法阶段，待评估

---

## Technical Debt

### P1 — Logger Rotation

**描述**：当前 `src/logger/logger.py` 使用 `FileHandler`，日志文件 `logs/app.log` 会无限增长。应改用 `RotatingFileHandler`，按文件大小自动切分（如 10 MB / 保留 5 个历史文件）。

**影响**：生产环境长时间运行会磁盘占满。

**目标版本**：V2.3

---

### P1 — Config YAML

**描述**：当前配置使用 Python 模块常量（`src/config/config.py`）。YAML 配置文件更易于非开发者修改（运维 / 分析师），且支持环境切换。迁移路径：创建 `config.yaml` + `src/config/loader.py`，保留 `config.py` 中的常量作为默认值。

**影响**：修改配置需要编辑 Python 代码。

**目标版本**：V2.3

---

### P1 — `print()` Removal in Business Modules

**描述**：`data_loader.py`、`data_cleaner.py`、`sales_analyzer.py`、`customer_analyzer.py`、`visualizer.py` 中仍有 `print()` 调用。V2 已建立 Logging System，应将这些 `print()` 替换为 `logger.info()`。唯一的例外是 `data_profiler.py`（其职责就是打印诊断报告）。

**影响**：CLI 输出和日志内容重复，且无法通过日志级别控制输出。

**目标版本**：V2.3

---

### P2 — Result Model 扩展

**描述**：`PipelineResult` 目前是简单的 dataclass，仅包装了 `sales_result` 和 `customer_result` 两个 dict。后续可以为 Sales 和 Customer 各自定义专门的 dataclass（`SalesResult`、`CustomerResult`），替代裸 dict，提升类型安全性。

**影响**：当前 dict 访问无 IDE 自动补全，字段名拼写错误只能在运行时发现。

**目标版本**：V3

---

### P2 — Config 结构扁平化

**描述**：当前 `src/config/config.py` 是扁平的模块级常量。后续可引入 namespace（如 `Config.paths.raw`、`Config.charts.dpi`）来组织配置项。

**影响**：随着配置项增多，扁平结构会变得难以管理。

**目标版本**：V3

---

### P2 — `pytest.ini` → `pyproject.toml`

**描述**：当前 pytest 配置在 `pyproject.toml` 的 `[tool.pytest.ini_options]` 中，这是推荐方式。如果后续有其他 pytest 配置需求（markers、filterwarnings），继续在此处添加。

**目标版本**：V2.3

---

## Future Roadmap

### V3 — Streamlit Dashboard

- Web 互动看板（Presentation Layer）
- Sidebar 导航 + 四页面（概览 / 销售 / 客户 / 上传）
- 互动过滤器（日期、国家、Top N）
- 调用 V2 Pipeline 作为后端

### V4 — Interactive Analytics

- Plotly 替换 Matplotlib（可交互图表）
- 高级过滤器（商品搜索、日期细粒度）
- 图表点击下钻

### V5 — AI Report

- LLM 集成（Anthropic / OpenAI）
- 英文叙述性分析报告
- 异常检测 + 自然语言查询
- PDF 导出

### V6 — Database Integration

- SQLite / PostgreSQL 替代 CSV
- SQLAlchemy ORM
- 数据 ETL Pipeline

### V7 — Deployment

- Docker 容器化
- GitHub Actions CI/CD
- Cloud Deploy（Streamlit Cloud / VPS）

---

## Completed Debt

### ✅ V2.2 — Type Hints

所有公开函数已添加完整类型标注。`data_loader.py`、`customer_analyzer.py`、`visualizer.py`、`report_generator.py` 的签名已修复。

### ✅ V2.2 — Config Path → Pathlib

`RAW_DATA_PATH`、`PROCESSED_DATA_PATH`、`REPORT_OUTPUT_PATH` 等路径常量已从 `str` 迁移至 `pathlib.Path`。

### ✅ V2.2 — PipelineResult Dataclass

`run_pipeline()` 不再返回裸 `dict`，改为返回 `PipelineResult` dataclass。
