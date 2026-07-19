# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [3.1.0] — 2026-07-19

### Added
- `src/ui/` package — 7 个模块（components, upload, analysis, charts, report, about）
- CSV 上传校验（必需列检测 + 编码自动识别）
- 交互式过滤器：国家多选 + Top N 滑块（分析概览页）
- 执行耗时显示（`time.perf_counter()`）
- `assets/` 目录（截图 + 架构图占位）

### Changed
- `app.py` 重构为薄壳路由（185 行 → 50 行），页面逻辑移至 `src/ui/`
- 可复用组件抽取至 `src/ui/components.py`
- 版本号升级至 3.1.0

## [3.0.0] — 2026-07-19

### Added
- Streamlit Web 展示层（`app.py`）— 第二个 Presentation Layer 入口
- 5 页面导航：数据上传、分析概览、图表展示、报告下载、关于
- CSV 文件上传功能（可替换默认数据源）
- KPI 指标卡片（总营收、订单数、客户数、客单价）
- 8 张图表展示（`st.image()` + 2 列网格布局）
- HTML 报告在线预览 + 下载（`st.download_button()`）

### Changed
- 版本号升级至 3.0.0（V3 Streamlit 里程碑）
- `requirements.txt` 新增 `streamlit`

## [2.3.0] — 2026-07-18

### Added
- YAML 配置系统（`config/config.yaml` + `src/config/loader.py`）
- `SalesResult`、`CustomerResult` dataclass（`src/models/`）
- ADR 文档（`docs/decisions/ADR-001 ~ 004`）
- `CHANGELOG.md`

### Changed
- `PipelineResult` 拆分为独立文件，字段类型从 `dict` 升级为 `SalesResult` / `CustomerResult`
- `main.py` 改用 `load_config()` 加载配置
- 版本号升级至 2.3.0

## [2.2.0] — 2026-07-18

### Added
- 全局 Type Hints（所有公开函数 100% 覆盖）
- pytest 测试体系（15 tests, 3 模块）
- Black + Ruff 代码质量工具（`pyproject.toml`）
- `PipelineResult` dataclass（`src/models/`）
- `TECH_DEBT.md`

### Changed
- Config 路径从 `str` 迁移至 `pathlib.Path`
- `run_pipeline()` 参数类型支持 `str | Path`
- 版本号升级至 2.2.0

## [2.1.0] — 2026-07-18

### Added
- Config System（`src/config/` — Python 常量）
- Logging System（`src/logger/` — 控制台 + 文件双输出）
- Exception System（`src/exceptions/` — 6 类异常）
- Pipeline 模块（`src/pipeline/` — 流程编排）

### Changed
- `main.py` 精简为薄壳入口（40 行 → 20 行）
- 硬编码路径迁移至 Config
- `print()` 关键节点替换为 logger

## [1.0.0] — 2026-07-17

### Added
- DataLoader（CSV → DataFrame，latin1 编码）
- DataProfiler（数据质量诊断：缺失值、重复、异常值、内存）
- DataCleaner（6 步清洗：去重 → 去空 → 去负 → 去零 → 类型转换 → TotalSales）
- SalesAnalyzer（总营收 $8.89M、18.5K 订单、月度趋势、Top 10）
- CustomerAnalyzer（RFM 分层，百分位打分，4,338 客户）
- Visualizer（8 张 Matplotlib 图表，Agg 后端，中文字体）
- ReportGenerator（自包含 HTML 报告，base64 内嵌图片）

[2.3.0]: https://github.com/Corn555/cross-border-dashboard/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/Corn555/cross-border-dashboard/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/Corn555/cross-border-dashboard/compare/v1.0.0...v2.1.0
[1.0.0]: https://github.com/Corn555/cross-border-dashboard/releases/tag/v1.0.0
