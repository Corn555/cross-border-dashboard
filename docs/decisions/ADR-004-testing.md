# ADR-004: Testing Strategy

**Status**: Accepted
**Date**: 2026-07-18

## Context

V1 无自动化测试，依赖手工运行 `python main.py` 验证。V2 开始需要建立测试体系，确保重构不影响分析结果。

## Decision

采用 **pytest + 手工迷你数据集** 的测试策略：

1. 测试框架：**pytest**（社区标准，简洁的 assert）
2. 测试数据：**conftest.py 中的迷你 DataFrame**（5-10 行手工构造），不依赖真实 `data/raw/sales.csv`
3. 测试范围：
   - Data Layer: 数据加载、清洗逻辑
   - Business Layer: 销售 KPI 计算、客户 RFM 计算
   - Service Layer: Config 加载与校验
4. 不测试：
   - Matplotlib 图表（二进制输出，验证 ROI 低）
   - Streamlit UI（UI 测试 ROI 低，V3 阶段手动验证）
   - data_profiler（纯 print 输出，适合重构后测试）

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| 真实 CSV 文件 | 测试依赖外部文件，CI 需要携带大数据集 |
| unittest (stdlib) | 语法冗长，社区已转向 pytest |
| 100% 覆盖率 | 1 人项目 ROI 低；UI/图表代码的自动化测试成本高于收益 |
| doctest | 仅适合简单函数；复杂 DataFrame 操作不适合 |

## Consequences

- **优点**: 测试不依赖外部文件；CI 可直接运行；重构有安全网
- **缺点**: 迷你数据集可能遗漏边界条件（如大量重复值导致的 qcut 问题）
