# 项目路线图

## V1.0 — 本地数据分析 ✅ DONE

**目标**：完成完整的数据分析管道。所有模块通过 `main.py` 一键运行，
输出终端报告 + HTML 报告 + 图表文件。

**技术栈**：Python, Pandas, NumPy, Matplotlib

### 里程碑

| # | 模块 | 交付物 | 状态 |
|---|--------|------------|------|
| M1 | DataProfiler | 数据质量诊断报告（终端输出） | ✅ |
| M2 | DataCleaner | `data/processed/sales_clean.csv` | ✅ |
| M3 | SalesAnalyzer | 销售 KPI + 图表数据（总营收 $8.89M、18.5K 订单） | ✅ |
| M4 | CustomerAnalyzer | RFM 客户分层 + 地理分布（4,338 客户、三层分级） | ✅ |
| M5 | Visualizer | 8 张 Matplotlib 图表 → `output/charts/` | ✅ |
| M6 | ReportGenerator | 自包含 HTML 报告 → `output/reports/report.html` | ✅ |

**V1 成果**：7 个 src 模块、6 个 commit、一键运行 `python main.py` 输出完整分析。

---

## V2.0 — 互动看板 🚧 规划中

**目标**：将终端输出升级为 Web 互动看板。

**技术栈新增**：Streamlit, Plotly（可选）

### 计划功能

- Streamlit Web 应用，侧边栏导航
- 互动过滤器：日期范围、国家多选、商品搜索
- 动态图表（缩放、悬停提示）
- 数据上传：支持用户上传自己的 CSV 文件
- 配置文件（`config.yaml`）管理路径和参数

### 里程碑

| # | 模块 | 描述 |
|---|---------|------------|
| M7 | Streamlit 框架 | 基础应用，页面结构和导航 |
| M8 | 互动过滤器 | 日期选择器、国家多选、商品搜索 |
| M9 | 动态图表 | 用 Plotly 替换 Matplotlib PNG |
| M10 | 文件上传 | 允许用户上传自定义数据集 |
| M11 | 配置系统 | YAML 配置文件管理所有路径和参数 |

---

## V3.0 — AI 智能分析 🚧 规划中

**目标**：集成 AI 生成叙述性分析报告和深度洞察。

**技术栈新增**：OpenAI API / Anthropic Claude API

### 计划功能

- 英文叙述性报告：AI 自动生成关键发现总结
- 异常检测：AI 标记数据中的异常模式
- 自然语言查询："德国 Q4 的销售情况如何？" → 自动生成图表
- PDF 导出：精美排版的多页 PDF 报告
- 邮件定时发送报告

### 里程碑

| # | 模块 | 描述 |
|---|---------|------------|
| M12 | AI 摘要 | 从分析结果自动生成英文叙述 |
| M13 | 异常检测 | AI 发现并解释数据异常 |
| M14 | 自然语言查询 | 文本输入 → 自动生成图表 |
| M15 | PDF 导出 | 精美多页 PDF 报告 |
| M16 | 定时发送 | 自动化定时报告生成 |

---

## 版本总览

```
V1.0  ✅  终端 + 文件输出     ──  Python CLI（当前）
V2.0  🚧  Web 互动看板       ──  Streamlit + Plotly
V3.0  🚧  AI 智能报告        ──  LLM API + PDF
```
