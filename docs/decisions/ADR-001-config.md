# ADR-001: Config System Design

**Status**: Accepted
**Date**: 2026-07-18

## Context

项目需要集中管理所有可配置参数（路径、图表参数、项目元数据）。V1 硬编码所有值。V2 需要支持配置修改而无需改动代码。

## Decision

采用 **Python 默认值 + YAML 可选覆盖** 的双层架构：

1. `src/config/config.py` — Python 模块常量，作为默认值和向后兼容层
2. `config/config.yaml` — YAML 文件，用户可修改来覆盖默认值
3. `src/config/loader.py` — `load_config()` 读取 YAML + merge 默认值

```python
from src.config import load_config
cfg = load_config()  # YAML 存在 → 覆盖默认值；YAML 缺失 → 纯默认值
```

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| 仅 YAML | 首次克隆无 YAML 文件会崩溃；无法 `from X import` |
| 仅 Python | 无法做到"改配置不改代码" |
| .env + python-dotenv | 无结构，嵌套配置难以表达 |
| TOML (pyproject.toml) | pyproject.toml 职责是项目元数据，不宜混入业务配置 |

## Consequences

- **优点**: 向后兼容（`from src.config import RAW_DATA_PATH` 仍可用）；YAML 缺失不崩溃；结构化配置
- **缺点**: 两套配置需保持同步；新增配置项需同时更新 YAML 和 Python 默认值
