# ADR-002: Pipeline Architecture

**Status**: Accepted
**Date**: 2026-07-18

## Context

V1 的 `main.py` 直接 import 所有分析模块并顺序调用。随着 V3（Streamlit）、V7（API）的加入，需要有统一的流程编排层，避免入口文件重复编排逻辑。

## Decision

采用 **Application Service Layer（Pipeline）** 模式：

1. `src/pipeline/pipeline.py` — `run_pipeline()` 编排 6 个阶段
2. 所有入口（CLI / Streamlit / API）只调用 Pipeline，不直接调用分析模块
3. Pipeline 通过参数接收路径（依赖注入），不内部 import Config

```
main.py (CLI) ──→ run_pipeline(raw_data, processed, charts, report)
app.py  (V3)  ──→ run_pipeline(...)   ← 同一接口
api.py  (V7)  ──→ run_pipeline(...)   ← 同一接口
```

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| 每个入口各自编排 | 代码重复；流程变更需改多个文件 |
| Pipeline 直接读 Config | 耦合 Config 实现；测试时需要 mock 文件系统 |
| 用 Airflow/Prefect | 严重过度设计，1 人项目不需要 Workflow Engine |

## Consequences

- **优点**: 入口文件极简（~25 行）；V3/V7 复用同一 Pipeline；可独立测试 Pipeline
- **缺点**: Pipeline 是新增的抽象层；参数数量随阶段增加而增长
