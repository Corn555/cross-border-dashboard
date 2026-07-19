# Portfolio Assets

Screenshots and diagrams for the portfolio README.

## Screenshots

After starting the app (`streamlit run app.py`), capture each page:

| File | Page | What to capture |
|------|------|----------------|
| `screenshot_upload.png` | 数据上传 | File uploader + default data button |
| `screenshot_analysis.png` | 分析概览 | KPI cards + segment stats + filtered tables |
| `screenshot_charts.png` | 图表展示 | Chart grid (2-column layout) |
| `screenshot_report.png` | 报告下载 | Download button + HTML preview |
| `screenshot_about.png` | 关于 | Project info + architecture |

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   Presentation Layer                     │
│                                                         │
│   main.py (CLI)          app.py (Web)                   │
│   终端文本输出             Streamlit UI                   │
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
