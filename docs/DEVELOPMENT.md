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
- No `print()` inside `src/` modules except in the profiler (whose job IS
  printing). Use `return` for data, let `main.py` decide what to print.
- Use f-strings for formatting

### 2.3 Type Hints (Recommended)

```python
import pandas as pd

def load_data(file_path: str) -> pd.DataFrame | None:
    ...
```

Type hints are required for function signatures in new modules.

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

## 7. Testing (V2+)

V1 relies on manual verification (run `main.py` and inspect output).

V2 will add:
- `pytest` for unit tests
- One test file per source module under `tests/`
- Minimum 80% function coverage

## 8. Language Policy

- **代码标识符**（变量名、函数名、列名）：英文（PEP 8 要求）
- **注释 & docstring**：中文（便于理解和沟通）
- **Commit message**：英文（Conventional Commits 规范）
- **终端输出 & 报告**：中文（面向中文用户）
- **文档**（ARCHITECTURE, DEVELOPMENT, ROADMAP）：中文为主，技术术语保留英文
