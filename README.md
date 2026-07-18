# Cross-border E-commerce Sales Dashboard

跨境电商销售数据分析平台 — 我的第一个数据分析作品集项目。

## Overview

本项目分析跨境电商交易数据，回答以下业务问题：

- **销售分析**：营收趋势、季节性波动、国家市场表现
- **商品分析**：热销商品排行、退货率、商品品类洞察
- **客户分析**：客户地理分布、RFM 分层、客户生命周期价值

> V1.0 已完成并冻结：本地数据分析流程，一键运行输出完整 HTML 报告。
> V2.0 进行中：工程化升级（Config / Logging / Type Hints / 分层架构）。

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

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.12+ |
| Data | Pandas, NumPy | 3.x, 2.x |
| Visualization | Matplotlib | 3.11+ |
| Reports | HTML + CSS | — |
| Version Control | Git | 2.x |

## Project Structure

```
cross-border-dashboard/
├── data/
│   ├── raw/                # 原始 CSV（只读，不修改）
│   └── processed/          # 清洗后 CSV（程序生成）
├── output/
│   ├── charts/             # 生成的图表 PNG
│   └── reports/            # HTML 分析报告
├── src/                    # 源码模块（每模块一个职责）
│   ├── data_loader.py      # CSV → DataFrame
│   ├── data_profiler.py    # 数据质量诊断
│   ├── data_cleaner.py     # 数据清洗流程
│   ├── sales_analyzer.py   # 销售 KPI 与趋势
│   ├── customer_analyzer.py # RFM 客户分层
│   ├── visualizer.py       # Matplotlib 图表工厂
│   └── report_generator.py # HTML 报告组装
├── docs/                   # 架构与规范文档
│   ├── ARCHITECTURE.md     # 系统架构设计
│   └── DEVELOPMENT.md      # 开发规范
├── .gitignore               # Git 忽略规则
├── main.py                 # 入口 — 一键运行全流程
├── requirements.txt        # Python 依赖
├── ROADMAP.md              # 版本路线图
└── README.md               # 本文件
```

## Quick Start

```bash
# 1. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 放入原始数据
# 将 sales.csv 复制到 data/raw/sales.csv

# 4. 运行全流程
python main.py

# 5. 查看报告
# 浏览器打开 output/reports/report.html
```

## Version Progress

| Version | 主题 | 状态 |
|---------|------|------|
| V1.0 | Local Analytics — CLI + Matplotlib 报告 | ✅ DONE（已冻结） |
| V2.0 | Core Engineering — Config, Logging, Type Hints, 分层架构 | 🚧 Sprint 2.1 |
| V3.0 | Streamlit Dashboard — Web 互动看板 | 🚧 规划中 |
| V4.0 | Interactive Analytics — Plotly 动态图表 | 🚧 规划中 |
| V5.0 | AI Report — LLM 智能分析 | 🚧 规划中 |
| V6.0 | Database Integration — 数据持久化 | 🚧 规划中 |
| V7.0 | Deployment — Docker + Cloud | 🚧 规划中 |

> V1 已冻结（Version Freeze），除 Bug Fix 外不再新增功能。详见 [ROADMAP.md](ROADMAP.md)。

## Documentation

- [V1 系统架构](docs/ARCHITECTURE.md)（已冻结）
- [V2+ 系统架构](docs/ARCHITECTURE_V2.md)（分层模型 + 设计原则）
- [开发规范](docs/DEVELOPMENT.md)
- [Config 设计方案](docs/CONFIG_DESIGN.md)
- [版本路线图](ROADMAP.md)
