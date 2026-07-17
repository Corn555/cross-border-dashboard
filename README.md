# Cross-border E-commerce Sales Dashboard

A data analysis portfolio project simulating a cross-border e-commerce sales
dashboard for business intelligence and reporting.

## Overview

This project analyzes a cross-border e-commerce transaction dataset to answer
key business questions:

- **Sales**: revenue trends, seasonal patterns, country-level performance
- **Products**: best-sellers, return rates, product category insights
- **Customers**: geographic distribution, RFM segmentation, lifetime value

V1 focuses on local data analysis with Python. Future versions add an
interactive web dashboard and AI-generated reports.

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.12+ |
| Data | Pandas, NumPy | 3.x, 2.x |
| Visualization | Matplotlib | 3.11+ |
| Version Control | Git | 2.x |

## Project Structure

```
cross-border-dashboard/
├── data/
│   ├── raw/                # Original CSV (read-only)
│   └── processed/          # Cleaned CSVs (generated)
├── output/
│   ├── charts/             # Saved chart images
│   └── reports/            # Generated reports
├── src/                    # All source modules
│   ├── data_loader.py      # CSV → DataFrame
│   ├── data_profiler.py    # Data quality diagnosis
│   ├── data_cleaner.py     # Data cleaning pipeline
│   ├── sales_analyzer.py   # Sales KPIs & trends
│   ├── customer_analyzer.py # RFM segmentation
│   ├── visualizer.py       # Matplotlib chart factory
│   └── report_generator.py # Report assembly
├── docs/                   # Architecture & standards
│   ├── ARCHITECTURE.md
│   └── DEVELOPMENT.md
├── main.py                 # Entry point — run full pipeline
├── requirements.txt        # Python dependencies
├── ROADMAP.md              # Version roadmap
└── README.md               # This file
```

## Quick Start

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place raw data
# Copy sales.csv → data/raw/sales.csv

# 4. Run the pipeline
python main.py
```

## Documentation

- [Architecture & Module Design](docs/ARCHITECTURE.md)
- [Development Standards](docs/DEVELOPMENT.md)
- [Version Roadmap](ROADMAP.md)
