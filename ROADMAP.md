# Project Roadmap

## V1.0 — Local Data Analysis (Current)

**Goal**: Complete the full data analysis pipeline locally. Every module runs
from `main.py` and produces verifiable output in the terminal and as files.

**Tech**: Python, Pandas, NumPy, Matplotlib

### Milestones

| # | Module | Deliverable | Acceptance Criteria |
|---|--------|------------|---------------------|
| M1 | DataProfiler | Data quality report in terminal | Missing%, duplicate count, anomaly flags printed |
| M2 | DataCleaner | `data/processed/sales_clean.csv` | Before/after row count compared; no nulls, no negatives |
| M3 | SalesAnalyzer | Sales KPI dict + terminal summary | Revenue, monthly trend, top products, top countries printed |
| M4 | CustomerAnalyzer | RFM table + terminal summary | Customer segments printed; country distribution shown |
| M5 | Visualizer | 8 charts saved to `output/charts/` | All charts render correctly with titles, labels, legends |
| M6 | ReportGenerator | `output/reports/report.html` | Self-contained HTML report with all KPIs and embedded charts |

**Target**: 6 commits on `main`, one per milestone.

---

## V2.0 — Interactive Dashboard

**Goal**: Replace terminal output with a web-based interactive dashboard.

**Tech additions**: Streamlit, Plotly (optional)

### Planned Features

- Streamlit web app with sidebar navigation
- Interactive filters: date range, country, product
- Dynamic charts (zoom, hover tooltips)
- Data upload: upload your own CSV for analysis
- Configuration file (`config.yaml`) for paths and parameters

### Milestones

| # | Feature | Description |
|---|---------|------------|
| M7 | Streamlit Setup | Basic app with page structure and navigation |
| M8 | Interactive Filters | Date picker, country multi-select, product search |
| M9 | Dynamic Charts | Replace Matplotlib PNGs with Plotly interactive charts |
| M10 | File Upload | Allow users to upload their own dataset |
| M11 | Config System | YAML config for all paths and analysis parameters |

---

## V3.0 — AI-Powered Analysis

**Goal**: Integrate AI to generate narrative analysis reports and insights.

**Tech additions**: OpenAI API (or Anthropic Claude API)

### Planned Features

- English narrative report: AI-generated summary of key findings
- Anomaly detection: AI flags unusual patterns in the data
- Natural language query: "Show me sales in Germany for Q4" → auto-generated chart
- PDF export: polished report with charts + narrative
- Email report scheduling

### Milestones

| # | Feature | Description |
|---|---------|------------|
| M12 | AI Summary | Generate English narrative from analysis results |
| M13 | Anomaly Detection | AI identifies and explains data anomalies |
| M14 | NL Query | Text input → auto-generated chart |
| M15 | PDF Export | Polished multi-page PDF report |
| M16 | Scheduling | Automated report generation on a schedule |

---

## Version Summary

```
V1.0  ──  Terminal + File Output  ──  Python CLI
V2.0  ──  Web Dashboard           ──  Streamlit + Plotly
V3.0  ──  AI Reports              ──  LLM API + PDF
```
