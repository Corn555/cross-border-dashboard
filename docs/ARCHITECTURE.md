# Architecture Document

## 1. System Overview

```
┌──────────────────────────────────────────────────────────┐
│                        main.py                           │
│              (Pipeline Orchestrator)                     │
└────┬─────┬─────┬─────┬─────┬─────┬────────┐
     │     │     │     │     │     │        │
     ▼     ▼     ▼     ▼     ▼     ▼        ▼
┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
│ Loader ││Profiler││Cleaner ││ Sales  ││Customer││Visualiz│
│        ││        ││        ││Analyzer││Analyzer││  -er   │
└───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘
    │         │         │         │         │         │
    ▼         ▼         ▼         ▼         ▼         ▼
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────────┐
│ CSV  ││Diag. ││Clean ││Stats ││RFM   ││PNG / HTML│
│→ DF  ││Report││ CSV  ││Dict  ││Table ││Reports   │
└──────┘└──────┘└──────┘└──────┘└──────┘└──────────┘
```

**Architectural Style**: Pipeline (sequential data processing stages). Each
module reads its input from the previous stage and passes output to the next.
No module has side effects outside its designated output target.

## 2. Module Design

### 2.1 DataLoader (`data_loader.py`)

| Aspect | Detail |
|--------|--------|
| Responsibility | Read raw CSV into a DataFrame |
| Input | `data/raw/sales.csv` |
| Output | `pd.DataFrame` |
| Dependencies | None |
| Error Handling | Return `None` on failure, print error message |
| Status | **DONE** |

### 2.2 DataProfiler (`data_profiler.py`)

| Aspect | Detail |
|--------|--------|
| Responsibility | Diagnose data quality — report what's wrong, don't fix it |
| Input | `pd.DataFrame` |
| Output | Dict with keys: `row_count`, `col_count`, `missing_pct`, `duplicate_count`, `negative_qty_count`, `null_customer_count` |
| Dependencies | None |
| Status | **NEXT** |

### 2.3 DataCleaner (`data_cleaner.py`)

| Aspect | Detail |
|--------|--------|
| Responsibility | Clean the data: drop duplicates, drop null CustomerID, remove negative/zero Quantity rows, convert InvoiceDate to datetime, create `TotalSales` column (`Quantity * Price`) |
| Input | `pd.DataFrame` |
| Output | Cleaned `pd.DataFrame` saved to `data/processed/sales_clean.csv` |
| Dependencies | DataProfiler (reads profiler output for before/after comparison) |
| Logging | Print rows before → rows after → rows removed |

### 2.4 SalesAnalyzer (`sales_analyzer.py`)

| Aspect | Detail |
|--------|--------|
| Responsibility | Compute all sales KPIs and aggregations |
| Input | Cleaned `pd.DataFrame` |
| Output | Dict of analysis results: total revenue, monthly trends, top 10 products by revenue, top 10 countries by revenue, average order value |
| Dependencies | DataCleaner |

**Key metrics:**
- Total Revenue = `sum(Quantity * Price)`
- Monthly Revenue Trend = `groupby(month)['TotalSales'].sum()`
- Top 10 Products = `groupby(Description)['TotalSales'].sum().nlargest(10)`
- Top 10 Countries = `groupby(Country)['TotalSales'].sum().nlargest(10)`
- Return Rate = `(negative Quantity rows) / (total rows) * 100`

### 2.5 CustomerAnalyzer (`customer_analyzer.py`)

| Aspect | Detail |
|--------|--------|
| Responsibility | RFM segmentation and customer geography analysis |
| Input | Cleaned `pd.DataFrame` |
| Output | Dict of RFM segments, customer counts per country |
| Dependencies | DataCleaner |

**RFM Model:**
- **R**ecency: days since last purchase (lower is better)
- **F**requency: number of unique invoices (higher is better)
- **M**onetary: total spend (higher is better)
- Each dimension scored 1–4 (quartile), combined into a 3-digit RFM score
- Segments: High Value (R≥3, F≥3, M≥3), Mid Value, Low Value

### 2.6 Visualizer (`visualizer.py`)

| Aspect | Detail |
|--------|--------|
| Responsibility | Generate and save all charts using Matplotlib |
| Input | Analysis results from SalesAnalyzer + CustomerAnalyzer |
| Output | PNG files saved to `output/charts/` |
| Dependencies | SalesAnalyzer, CustomerAnalyzer |

**V1 Charts (8 total):**
1. Monthly Revenue Trend (line chart)
2. Top 10 Products by Revenue (horizontal bar)
3. Top 10 Countries by Revenue (horizontal bar)
4. Revenue by Country (pie chart — top 5 + "Others")
5. RFM Segment Distribution (bar chart)
6. Average Order Value Trend (line chart)
7. Quantity vs Revenue Scatter (scatter plot)
8. Top Customers by Spend (horizontal bar)

### 2.7 ReportGenerator (`report_generator.py`)

| Aspect | Detail |
|--------|--------|
| Responsibility | Assemble analysis results + charts into a single HTML report |
| Input | Analysis dicts + chart image paths |
| Output | `output/reports/report.html` |
| Dependencies | All upstream modules |

## 3. Data Flow

```
data/raw/sales.csv
        │
        ▼
   [DataLoader]         ← Read CSV → DataFrame
        │
        ▼
   [DataProfiler]       ← Diagnose: print quality report
        │
        ▼
   [DataCleaner]        ← Clean → data/processed/sales_clean.csv
        │
        ├──────────────────┐
        ▼                  ▼
   [SalesAnalyzer]   [CustomerAnalyzer]
        │                  │
        └────────┬─────────┘
                 ▼
          [Visualizer]     ← Generate charts → output/charts/*.png
                 │
                 ▼
        [ReportGenerator]  ← Assemble → output/reports/report.html
```

## 4. Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Module coupling | Each module receives DataFrame, returns dict | Easy to test independently, easy to swap implementations |
| Output format | Dict (not class) | Simple, serializable, no OOP overhead for V1 |
| File I/O | Only Loader reads files, only Cleaner writes data | Clear boundaries, no scattered file access |
| Charts | Save to files, not plt.show() | Headless execution, reusable in reports |
| Language | Code & comments in English | Portfolio project for international audience |
| Config | Hard-coded paths in V1 | Premature abstraction; add config file in V2 |

## 5. Directory Rationale

- `data/raw/` — Never modified. Original data treated as immutable.
- `data/processed/` — Generated by cleaner. Git-ignored.
- `output/` — All generated artifacts (charts, reports). Git-ignored.
- `src/` — One file per module. Flat structure since <10 files.
- `docs/` — Separated from code. Architecture and process docs live here.
