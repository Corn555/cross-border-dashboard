# Portfolio Assets

Screenshots and diagrams for the project portfolio.

## Screenshots

After starting the app (`streamlit run app.py`), capture each page:

| File | Page | Description |
|------|------|-------------|
| `dashboard-home.png` | 分析概览 | KPI cards + RFM segments + filtered tables |
| `upload-page.png` | 数据上传 | CSV uploader + validation + run button |
| `analysis-page.png` | 分析概览 | Interactive filters (country + Top N) |
| `charts-page.png` | 图表展示 | 8 charts in 2-column grid |
| `report-page.png` | 报告下载 | Download button + HTML preview |
| `architecture.png` | — | Four-layer architecture diagram |

Optional: `demo.gif` — screen recording of the full workflow.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   Presentation Layer                     │
│                                                         │
│   main.py (CLI)          app.py (Web)                   │
│   Terminal output         Streamlit UI                   │
│                                                         │
│   Both call the same run_pipeline() interface           │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                 Application Layer                        │
│                                                         │
│   src/pipeline/pipeline.py                              │
│   run_pipeline(raw_data, processed_data,                │
│                charts_output_dir, report_output_path)   │
│   -> PipelineResult                                     │
│                                                         │
│   6 phases: Load -> Profile -> Clean -> Analyze         │
│            -> Visualize -> Report                       │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌─────▼─────┐ ┌─────▼──────────────┐
│ Business     │ │ Data      │ │ Infrastructure     │
│              │ │           │ │                    │
│ sales_       │ │ data_     │ │ src/config/       │
│   analyzer   │ │   loader  │ │ src/logger/       │
│ customer_    │ │ data_     │ │ src/exceptions/   │
│   analyzer   │ │   profiler│ │ src/models/       │
│ visualizer   │ │ data_     │ │ src/ui/           │
│ report_      │ │   cleaner │ │                    │
│   generator  │ │           │ │                    │
└──────────────┘ └───────────┘ └────────────────────┘
```
