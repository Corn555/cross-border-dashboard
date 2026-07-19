# ADR-003: Exception Hierarchy

**Status**: Accepted
**Date**: 2026-07-18

## Context

V1 使用 `return None` 表示失败，调用方需要检查返回值。这种方式容易遗漏检查，且无法传递失败原因。需要统一的错误处理机制。

## Decision

采用 **类型化异常层级**：

```
ProjectError (基类)
├── DataLoadError       — 数据加载失败
├── DataCleanError      — 数据清洗失败
├── AnalysisError       — 分析计算失败
├── VisualizationError  — 图表生成失败
└── ReportGenerationError — 报告生成失败
```

使用规则：
- **Data 层**: 可以 raise，不吞异常
- **Business 层**: 不 raise 也不 catch（假设输入合法）
- **Service 层 (Pipeline)**: 捕获原始异常 → 转为 ProjectError 子类 → 向上抛
- **Presentation 层 (main.py)**: `except ProjectError` → logger.exception() → exit

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| 统一用 ValueError | 无法区分错误来源（是数据加载失败还是分析失败？） |
| return None | 无法传递错误上下文；调用方容易遗漏检查 |
| 每个模块自定义异常 | 无公共基类，调用方需要 5 个 except 分支 |

## Consequences

- **优点**: 调用方只需 `except ProjectError`；异常类型指示失败阶段；保留原始 traceback
- **缺点**: 6 个异常类对于 1 人项目显得正式；Pipeline 中每个阶段都要 try/except
