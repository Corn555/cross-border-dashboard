# Development Standards

## 1. Environment

- Python 3.12+
- Virtual environment in `.venv/` (git-ignored)
- Install: `pip install -r requirements.txt`
- Add new dependencies: `pip install <package> && pip freeze > requirements.txt`

## 2. Python Coding Standards

### 2.1 Style
- **PEP 8** — 4 spaces, 79-char lines (100 for docstrings and comments)
- **Naming**: `snake_case` for functions/variables, `UPPER_CASE` for constants,
  `PascalCase` for classes (if any)
- **Imports**: stdlib → third-party → local, each group separated by a blank
  line

### 2.2 Functions

Every public function follows this template (**comments & docstrings in Chinese**,
code identifiers in English):

```python
def do_something(dataframe, param):
    """
    函数功能简述。

    Args:
        dataframe (pd.DataFrame): 输入数据。
        param (int): 阈值。

    Returns:
        dict: 返回字段说明。
    """
    # 具体实现
    return result
```

Rules:
- One function = one responsibility
- Max 30 lines per function; if longer, split into helpers
- No `print()` inside `src/` modules — 使用 `logger.info()` / `logger.warning()` / `logger.error()` 替代（参见 §9 Logging）。例外：`data_profiler.py` 的职责是终端报告，可保留 `print()`。
- Use f-strings for formatting

### 2.3 Type Hints (Required)

```python
import pandas as pd

def load_data(file_path: str) -> pd.DataFrame | None:
    ...
```

Type hints are **required** for ALL function signatures in `src/` modules。
V2 起新代码零容忍无类型标注，CI 中通过 `mypy --strict` 检查。

## 3. Module Template

Every new `src/` module must follow this skeleton:

```python
"""
Module: <name>
Responsibility: <one-line summary>
"""
import pandas as pd
import numpy as np


def <main_function>(df: pd.DataFrame) -> dict:
    """
    <What it does>

    Args:
        df: Input DataFrame.

    Returns:
        dict: <describe returned keys>
    """
    result = {}
    # Implementation
    return result
```

- One primary public function per module (named after the module's job)
- Private helpers prefixed with `_`
- Module can be `python -m src.module_name` for standalone testing

## 4. Git Workflow

### 4.1 Branch Strategy

```
main
  │
  ├── feature/<module-name>   ← One branch per module (V2+)
  │
  └── (direct commits in V1)  ← V1 is solo dev, commit directly to main
```

V1 is solo development on `main`. V2+ will use feature branches.

### 4.2 Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short description>

<body — optional, for context>
```

| Type | When to use |
|------|------------|
| `feat:` | New module or feature |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `refactor:` | Code changes without feature change |
| `style:` | Formatting, whitespace (no logic change) |
| `chore:` | Build, deps, config |

**Rules:**
- Commit message in English, imperative mood ("add", not "added")
- One commit per module completion
- Commit only when the module passes its Definition of Done
- Never commit broken code to `main`

### 4.3 What NOT to commit

Listed in `.gitignore`:
- `.venv/`
- `__pycache__/`
- `data/processed/` (generated)
- `output/` (generated)
- `.env` files

## 5. Definition of Done (per module)

A module is "done" when ALL of these are true:

- [ ] Code written and follows the module template above
- [ ] Module can run independently (callable from `main.py`)
- [ ] Output is clear and matches the spec in ARCHITECTURE.md
- [ ] No `print()` outside of profiler modules (return data, don't print it)
- [ ] `main.py` updated to call the new module
- [ ] `python main.py` runs end-to-end without errors
- [ ] One commit with a conventional commit message

## 6. Code Review Checklist

Before committing any module, self-review against this list:

1. **Correctness**: Does it compute what it claims to compute?
2. **Edge Cases**: What happens with empty data? Nulls? Zero values?
3. **Performance**: Is it vectorized (Pandas) rather than row-by-row loops?
4. **Readability**: Can someone else understand it in 2 minutes?
5. **No Dead Code**: No commented-out code, no unused imports

## 7. Testing

V1 relies on manual verification (run `main.py` and inspect output).

### 7.1 Test Framework

- **pytest** — 社区标准，简洁的 assert 语法
- 测试目录：`tests/`
- 命名规则：`test_<module_name>.py`
- 运行：`pytest tests/`（项目根目录）

### 7.2 Test Structure

```
tests/
├── __init__.py
├── conftest.py             # 共享 fixture（示例数据、mock 配置）
├── test_sales_analyzer.py
├── test_customer_analyzer.py
├── test_data_cleaner.py
└── test_config.py          # V2 新增
```

### 7.3 Test Principles

- 每个 V1 分析模块至少一个测试文件
- 使用 conftest.py 中的共享 fixture 提供测试用 DataFrame
- 测试数据为手工构造的小数据集（5-10 行），不依赖真实 data/raw/sales.csv
- 不测试绘图函数（Matplotlib 输出为二进制，验证方式复杂）
- Config 模块测试：验证 YAML 解析正确性
- Service 层测试：使用 mock 避免真实文件 I/O

### 7.4 Fixture 示例

```python
# conftest.py
import pandas as pd
import pytest

@pytest.fixture
def sample_sales_df():
    """构造一个迷你清洗后数据集用于测试。"""
    data = {
        "Invoice": ["001", "002", "003"],
        "Customer ID": [1, 2, 1],
        "Quantity": [2, 1, 5],
        "Price": [10.0, 20.0, 15.0],
        "TotalSales": [20.0, 20.0, 75.0],
        "InvoiceDate": pd.to_datetime(["2025-01-15", "2025-02-20", "2025-03-10"]),
        "Country": ["UK", "Germany", "UK"],
    }
    return pd.DataFrame(data)
```

## 8. Language Policy

- **代码标识符**（变量名、函数名、列名）：英文（PEP 8 要求）
- **注释 & docstring**：中文（便于理解和沟通）
- **Commit message**：英文（Conventional Commits 规范）
- **终端输出 & 报告**：中文（面向中文用户）
- **文档**（ARCHITECTURE, DEVELOPMENT, ROADMAP）：中文为主，技术术语保留英文

## 9. V2 — Logging Standards

### 9.1 Logger 初始化

`src/logger.py` 暴露一个 `setup_logging()` 函数，在 `main.py` 启动时调用一次：

```python
# main.py
from src.logger import setup_logging
from src.config import load_config

cfg = load_config()
setup_logging(cfg)
```

### 9.2 模块内使用

```python
import logging

logger = logging.getLogger(__name__)


def load_data(file_path: str) -> pd.DataFrame | None:
    logger.info("开始加载数据：%s", file_path)
    try:
        df = pd.read_csv(file_path, encoding="latin1")
        logger.info("数据加载成功，%d 行 %d 列", len(df), len(df.columns))
        return df
    except FileNotFoundError:
        logger.error("文件不存在：%s", file_path)
        raise DataLoadError(f"数据文件不存在: {file_path}")
```

### 9.3 规则

- 每个模块顶部定义 `logger = logging.getLogger(__name__)`
- 使用 `%s` / `%d` 占位符（lazy evaluation，避免不必要的字符串拼接）
- 不在 Business 层打 INFO 日志（Business 层是纯计算，只打 DEBUG/WARNING）
- Data 层打 INFO（I/O 操作需要记录）
- Service 层打 INFO（编排步骤需要记录）
- 异常捕获必须用 `logger.exception()` 输出完整 traceback

## 10. V2 — Exception Handling Standards

### 10.1 异常层级

```python
# src/exceptions.py

class CrossBorderDashboardError(Exception):
    """所有自定义异常的基类。"""

class ConfigError(CrossBorderDashboardError):
    """配置加载或校验失败。"""

class DataLoadError(CrossBorderDashboardError):
    """数据文件读取失败。"""

class DataCleanError(CrossBorderDashboardError):
    """数据清洗过程异常。"""

class AnalysisError(CrossBorderDashboardError):
    """分析计算异常。"""
```

### 10.2 使用规则

| 层 | 可以 raise | 可以 catch | 规则 |
|----|-----------|-----------|------|
| Data | ✅ | ✅ | I/O 失败 raise，不静默吞异常 |
| Business | ❌ | ❌ | 假设输入合法，不做防御式编程 |
| Service | ✅ | ✅ | 编排层 catch 下层异常，决定是否重试或降级 |
| Presentation | ❌ | ✅ | 顶层 try/except，展示用户友好信息 |

### 10.3 示例

```python
# ✅ Data 层：明确 raise
def load_data(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise DataLoadError(f"文件不存在: {file_path}")
    ...

# ❌ Data 层：return None（V1 风格，V2 禁止）
def load_data(file_path: str) -> pd.DataFrame | None:
    if not os.path.exists(file_path):
        return None  # 调用方不知道发生了什么
```

## 11. V2 — Service Layer Patterns

### 11.1 PipelineService

`src/pipeline_service.py` 是 V2 的核心编排模块：

```python
class PipelineService:
    """
    编排完整的数据分析流程。

    Attributes:
        config: 全局配置 dict。
    """

    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def run(self, data_path: str | None = None) -> dict:
        """执行全流程，返回完整分析结果。"""
        ...
```

### 11.2 设计原则

- Service 是有状态的（持有 config），Business 层是无状态的（纯函数）
- Service 方法可以调用多个 Business 模块并组合结果
- V3 中 Streamlit 通过同一个 Service 实例调用分步方法（如 `service.load_only()`）
- Service 不直接操作 DataFrame，通过 Business 层间接操作
