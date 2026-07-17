# 系统架构文档

## 1. 系统概览

```
┌──────────────────────────────────────────────────────────┐
│                        main.py                           │
│                   （流程编排器）                           │
└────┬─────┬─────┬─────┬─────┬─────┬────────┐
     │     │     │     │     │     │        │
     ▼     ▼     ▼     ▼     ▼     ▼        ▼
┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
│ Loader ││Profiler││Cleaner ││ Sales  ││Customer││Visualiz│
│ 加载器 ││ 诊断器 ││ 清洗器 ││ 分析器 ││ 分析器 ││  可视化 │
└───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘
    │         │         │         │         │         │
    ▼         ▼         ▼         ▼         ▼         ▼
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────────┐
│ CSV  ││诊断  ││清洗后││销售  ││RFM   ││ PNG/HTML │
│→ DF  ││报告  ││ CSV  ││指标  ││分层  ││  报告    │
└──────┘└──────┘└──────┘└──────┘└──────┘└──────────┘
```

**架构模式**：Pipeline（管道式顺序处理）。每个模块从前一阶段接收数据，处理后传递给下一阶段。
模块之间无直接耦合，仅通过 DataFrame / Dict 传递数据。

## 2. 模块设计

### 2.1 DataLoader（`data_loader.py`）

| 属性 | 说明 |
|--------|--------|
| 职责 | 读取原始 CSV 文件，返回 DataFrame |
| 输入 | `data/raw/sales.csv` |
| 输出 | `pd.DataFrame` |
| 依赖 | 无 |
| 容错 | 失败时返回 `None`，打印错误信息 |
| 状态 | ✅ DONE |

### 2.2 DataProfiler（`data_profiler.py`）

| 属性 | 说明 |
|--------|--------|
| 职责 | 诊断数据质量 — 发现并报告问题，不修改数据 |
| 输入 | `pd.DataFrame`（原始数据） |
| 输出 | Dict：包含行数、列数、缺失率、重复数、异常检测、内存占用等 |
| 依赖 | 无 |
| 状态 | ✅ DONE |

### 2.3 DataCleaner（`data_cleaner.py`）

| 属性 | 说明 |
|--------|--------|
| 职责 | 清洗原始数据：去重、去空 Customer ID、去负数量/零数量/零价格、类型转换、添加 TotalSales 计算列 |
| 输入 | `pd.DataFrame`（原始数据） |
| 输出 | 清洗后 `pd.DataFrame`，保存至 `data/processed/sales_clean.csv` |
| 依赖 | DataProfiler（用于前后对比） |
| 状态 | ✅ DONE |

**清洗结果**：541,910 → 392,693 行（移除 27.5% 脏数据）

### 2.4 SalesAnalyzer（`sales_analyzer.py`）

| 属性 | 说明 |
|--------|--------|
| 职责 | 计算全部销售 KPI 和聚合指标 |
| 输入 | 清洗后 `pd.DataFrame` |
| 输出 | Dict：总营收、订单数、客户数、客单价、月度趋势、Top 10 商品/国家 |
| 依赖 | DataCleaner |
| 状态 | ✅ DONE |

**核心指标**：
- 总营收 = `sum(Quantity * Price)` = **$8,887,227**
- 月度营收趋势 = `resample("ME")["TotalSales"].sum()`
- Top 10 商品 = `groupby("Description")["TotalSales"].sum().nlargest(10)`
- Top 10 国家 = `groupby("Country")["TotalSales"].sum().nlargest(10)`

### 2.5 CustomerAnalyzer（`customer_analyzer.py`）

| 属性 | 说明 |
|--------|--------|
| 职责 | RFM 客户分层 + 客户地理分布分析 |
| 输入 | 清洗后 `pd.DataFrame` |
| 输出 | Dict：RFM 表、分层统计（高/中/低价值）、国家客户分布 |
| 依赖 | DataCleaner |
| 状态 | ✅ DONE |

**RFM 模型**：
- **R**ecency（最近购买）：距最后交易天数（越短越好）
- **F**requency（购买频率）：独立订单数（越多越好）
- **M**onetary（消费金额）：总消费额（越高越好）
- 百分位排名法打分 1-4，组合为 RFM 分数
- 分层：高价值客户 29.8% / 中价值客户 39.9% / 低价值客户 30.2%

### 2.6 Visualizer（`visualizer.py`）

| 属性 | 说明 |
|--------|--------|
| 职责 | 基于分析结果生成全部 Matplotlib 图表 |
| 输入 | SalesAnalyzer + CustomerAnalyzer 的分析结果 dict |
| 输出 | 8 张 PNG 图表，保存至 `output/charts/` |
| 依赖 | SalesAnalyzer, CustomerAnalyzer |
| 状态 | ✅ DONE |

**V1 图表清单（8 张）**：
1. 月度营收趋势（折线图）
2. Top 10 商品按营收（横向柱状图）
3. Top 10 国家按营收（横向柱状图）
4. 各国营收占比（饼图 — Top 5 + 其他）
5. RFM 客户分层（柱状图）
6. 月度客单价趋势（折线图）
7. 订单数 vs 营收（散点图，按国家着色）
8. Top 客户消费排名（横向柱状图，按价值分层着色）

### 2.7 ReportGenerator（`report_generator.py`）

| 属性 | 说明 |
|--------|--------|
| 职责 | 将分析结果 + 图表整合为自包含的 HTML 报告 |
| 输入 | 分析 dict + 图表文件路径列表 |
| 输出 | `output/reports/report.html`（574 KB，内嵌 base64 图片） |
| 依赖 | 所有上游模块 |
| 状态 | ✅ DONE |

## 3. 数据流

```
data/raw/sales.csv
        │
        ▼
   [DataLoader]         ← 读取 CSV → DataFrame
        │
        ▼
   [DataProfiler]       ← 诊断：打印数据质量报告
        │
        ▼
   [DataCleaner]        ← 清洗 → data/processed/sales_clean.csv
        │
        ├──────────────────┐
        ▼                  ▼
   [SalesAnalyzer]   [CustomerAnalyzer]
        │                  │
        └────────┬─────────┘
                 ▼
          [Visualizer]     ← 生成图表 → output/charts/*.png
                 │
                 ▼
        [ReportGenerator]  ← 组装 → output/reports/report.html
```

## 4. 设计决策

| 决策 | 选择 | 理由 |
|----------|--------|-----------|
| 模块耦合方式 | 每个模块接收 DataFrame，返回 Dict | 可独立测试，易替换实现 |
| 输出格式 | Dict（不用 Class） | 简单、可序列化、V1 无需 OOP |
| 文件 I/O 边界 | 只有 Loader 读文件，Cleaner 写数据文件 | 边界清晰，不会散落各处读写 |
| 图表输出 | 保存为文件，不使用 plt.show() | 支持无头运行，可复用于报告 |
| 注释语言 | 中文（代码标识符英文） | 面向中文开发者，PEP 8 兼容 |
| 配置方式 | V1 硬编码路径 | 避免过早抽象，V2 引入 config.yaml |

## 5. 目录说明

- `data/raw/` — 原始数据，绝不修改，视为不可变
- `data/processed/` — 清洗后数据，程序生成，git-ignored
- `output/` — 所有生成产物（图表、报告），git-ignored
- `src/` — 每模块一个文件，扁平结构（< 10 文件无需子目录）
- `docs/` — 与代码分离，架构和流程文档
