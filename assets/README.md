# Assets

Demo screenshots and architecture diagrams for the project portfolio.

## Add Your Screenshots

After running `streamlit run app.py`, capture screenshots of each page:

- `screenshot_upload.png` — Data upload page
- `screenshot_analysis.png` — Analysis overview with KPI cards
- `screenshot_charts.png` — Chart grid display
- `screenshot_report.png` — HTML report preview + download
- `screenshot_about.png` — About page

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   Presentation Layer                     │
│                                                         │
│   main.py (CLI)          app.py (Web)                   │
│   终端文本输出             Streamlit UI                   │
│                                                         │
│   两者调用同一个 run_pipeline() 接口                        │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                 Application Layer                        │
│                                                         │
│   src/pipeline/pipeline.py                              │
│   run_pipeline(raw_data, processed_data,                │
│                charts_output_dir, report_output_path)   │
│   → PipelineResult                                      │
│                                                         │
│   6 阶段编排：Load → Profile → Clean → Analyze          │
│              → Visualize → Report                       │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌─────▼─────┐ ┌─────▼──────────────┐
│ Business     │ │ Data      │ │ Infrastructure     │
│              │ │           │ │                    │
│ sales_analyzer│ │data_loader│ │ src/config/       │
│ customer_    │ │ data_     │ │ src/logger/       │
│   analyzer   │ │ profiler  │ │ src/exceptions/   │
│ visualizer   │ │ data_     │ │ src/models/       │
│ report_      │ │ cleaner   │ │ src/ui/           │
│   generator  │ │           │ │                    │
└──────────────┘ └───────────┘ └────────────────────┘
```
