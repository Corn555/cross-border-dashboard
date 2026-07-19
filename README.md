# Cross-border E-commerce Sales Dashboard

跨境电商销售数据分析平台 — 我的第一个数据分析作品集项目。

## Overview

本项目分析跨境电商交易数据，回答以下业务问题：

- **销售分析**：营收趋势、季节性波动、国家市场表现
- **商品分析**：热销商品排行、退货率、商品品类洞察
- **客户分析**：客户地理分布、RFM 分层、客户生命周期价值

> V1.0 已冻结。V2.3 完成工程化升级。V3.0 新增 Streamlit Web 展示层。

## Architecture

```
Presentation Layer    main.py (CLI) + app.py (Web)  ← 双入口
    │
Application Layer    src/pipeline/              ← 流程编排
    │
Business Layer       sales_analyzer, customer_analyzer,
                     visualizer, report_generator  ← 纯计算
    │
Data Layer           data_loader, data_cleaner  ← I/O
    │
Infrastructure       src/config/, src/logger/, src/exceptions/, src/models/
```

## V1.0 Results

| 指标 | 数值 |
|------|------|
| 清洗后交易记录 | 392,693 行 |
| 总营收 | $8,887,227 |
| 总订单 | 18,532 |
| 总客户 | 4,338 |
| 平均客单价 | $480 |
| 高价值客户占比 | 29.8% |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12+ |
| Data | Pandas, NumPy |
| Visualization | Matplotlib |
| Reports | HTML + CSS (self-contained, base64 images) |
| Code Quality | Black, Ruff |
| Testing | pytest |
| Version Control | Git |

## Project Structure

```
cross-border-dashboard/
├── app.py                # Streamlit Web 入口（V3 新增）
├── main.py               # CLI 入口
├── src/
│   ├── config/           # 全局配置（Path 对象）
│   ├── logger/           # 统一日志系统（控制台 + 文件）
│   ├── exceptions/       # 自定义异常体系（6 类）
│   ├── models/           # 数据模型（PipelineResult dataclass）
│   ├── pipeline/         # 流程编排（6 阶段 Pipeline）
│   ├── data_loader.py    # Data Layer — CSV → DataFrame
│   ├── data_profiler.py  # Data Layer — 数据质量诊断
│   ├── data_cleaner.py   # Data Layer — 6 步清洗
│   ├── sales_analyzer.py # Business Layer — 销售 KPI
│   ├── customer_analyzer.py  # Business Layer — RFM 分层
│   ├── visualizer.py     # Business Layer — 8 张图表
│   └── report_generator.py   # Business Layer — HTML 报告
├── tests/                # 单元测试（pytest）
│   ├── conftest.py
│   ├── test_data_loader.py
│   ├── test_data_cleaner.py
│   └── test_sales_analyzer.py
├── docs/                 # 架构与规范文档
├── data/                 # 原始 + 处理后数据
├── output/               # 生成产物（图表 + 报告）
├── logs/                 # 运行日志
├── main.py               # CLI 入口
├── pyproject.toml        # 项目配置（Black, Ruff, pytest）
├── TECH_DEBT.md          # 技术债务 & 未来路线图
├── ROADMAP.md            # 版本路线图
└── README.md
```

## How to Run

```bash
# 1. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 放入原始数据 — 将 sales.csv 复制到 data/raw/sales.csv

# 4. 运行（二选一）
# CLI 模式
python main.py
# Web 模式（Streamlit）
streamlit run app.py

# 5. 查看报告 — 浏览器打开 output/reports/report.html
```

## How to Test

```bash
# 运行全部测试
pytest tests/

# 带详细输出
pytest tests/ -v

# 运行单个测试文件
pytest tests/test_sales_analyzer.py -v
```

## How to Format Code

```bash
# 代码格式化
black src/ tests/ main.py

# 代码检查
ruff check src/ tests/ main.py

# 自动修复
ruff check --fix src/ tests/ main.py
```

## How to Add a New Module

1. **确定模块归属层** — 参照 [ARCHITECTURE_V2.md](docs/ARCHITECTURE_V2.md) 的四层模型
2. **创建源文件** — `src/<layer>/<module>.py`，遵循 [DEVELOPMENT.md](docs/DEVELOPMENT.md) 模板
3. **添加类型标注** — 所有公共函数签名必须有完整 type hints
4. **使用 Logger** — `logger = get_logger(__name__)`，不用 `print()`
5. **编写测试** — `tests/test_<module>.py`，使用 conftest.py 的 fixture
6. **更新文档** — 如涉及架构变更，更新相关 docs/
7. **运行全量验证** — `pytest && ruff check && python main.py`

## Version Progress

| Version | 主题 | 状态 |
|---------|------|------|
| V1.0 | Local Analytics | ✅ 已冻结 |
| V2.3 | Core Engineering — YAML Config, Result Models, ADR | ✅ 已完成 |
| V3.0 | Streamlit Dashboard | ✅ 当前 |
| V4.0 | Interactive Analytics — Plotly | 🚧 规划中 |
| V5.0 | AI Report — LLM | 🚧 规划中 |
| V6.0 | Database Integration | 🚧 规划中 |
| V7.0 | Deployment — Docker + Cloud | 🚧 规划中 |

## V3.0 — Streamlit Dashboard

V3 在 V2 的工程基础上叠加了 Web 展示层，核心架构不变：

```
app.py (Streamlit)  —— Presentation Layer（新增，零业务逻辑）
    │
src/pipeline/       —— Application Layer（复用 V2，零改动）
    │
src/ models, config, logger, exceptions  —— Infrastructure（复用 V2）
```

- **Sidebar 导航**：数据上传 / 分析概览 / 图表展示 / 报告下载 / 关于
- **CSV 上传**：支持替换默认数据源，上传后直接运行 Pipeline
- **KPI 卡片**：总营收、订单数、客户数、客单价（`st.metric()`）
- **图表展示**：8 张图表以 2 列网格展示（`st.image()`）
- **报告下载**：HTML 在线预览 + 一键下载（`st.download_button()`）
- **配置驱动**：所有路径和参数从 `config/config.yaml` 读取

```bash
streamlit run app.py
```

## Documentation

- [V1 系统架构](docs/ARCHITECTURE.md)（已冻结）
- [V2+ 系统架构](docs/ARCHITECTURE_V2.md)（分层模型 + 设计原则）
- [开发规范](docs/DEVELOPMENT.md)
- [Config 设计方案](docs/CONFIG_DESIGN.md)
- [架构决策记录](docs/decisions/)（ADR-001 ~ 004）
- [更新日志](CHANGELOG.md)
- [技术债务 & 路线图](TECH_DEBT.md)
- [版本路线图](ROADMAP.md)
