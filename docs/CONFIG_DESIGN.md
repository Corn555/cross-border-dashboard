# Config 设计方案（V2）

## 1. 设计目标

集中管理所有可配置参数，消除硬编码。覆盖范围：文件路径、图表参数、UI 设置、过滤条件默认值。

**不在 Config 中管理的：**
- 业务逻辑参数（如 RFM 百分位分界点 0.25/0.5/0.75 — 属于分析模型，不应随意调整）
- 数据列名（由输入 CSV 结构决定，配置化无意义）
- 一次性魔数（如 HTML 报告的 max-width: 1000px — 属于 UI 样式细节）

## 2. Schema 设计

```yaml
# config.yaml — 全局配置文件
# 修改此文件后重启 Streamlit 即可生效

# ── 文件路径 ──────────────────────────────────
paths:
  raw_data: "data/raw/sales.csv"           # 默认数据源
  processed_dir: "data/processed"          # 清洗后数据目录
  charts_dir: "output/charts"             # 图表输出目录
  reports_dir: "output/reports"           # 报告输出目录

# ── UI 设置 ────────────────────────────────────
ui:
  page_title: "跨境电商销售数据分析平台"       # 浏览器标签标题
  page_icon: "📊"                           # 浏览器标签图标
  layout: "wide"                            # centered | wide
  sidebar_title: "导航"                     # 侧边栏标题
  default_page: "概览"                       # 启动时默认页面

# ── 图表参数 ───────────────────────────────────
charts:
  figure_size: [12, 6]                     # 默认图表尺寸 (宽, 高) 英寸
  dpi: 120                                 # 输出分辨率
  color_palette: "tab10"                   # Matplotlib 调色板名
  font_family: "Microsoft YaHei"           # 图表字体（中文优先）
  fallback_font: "SimHei"                  # 备选字体
  top_n_default: 10                        # Top N 排行默认数量

# ── 过滤条件默认值 ─────────────────────────────
filters:
  date_range: null                         # 默认日期范围：null = 全部
  countries: []                            # 默认国家选择：[] = 全部
  date_format: "%Y-%m-%d"                  # 日期显示格式

# ── 缓存设置 ───────────────────────────────────
cache:
  ttl_seconds: 3600                        # 缓存有效期（秒），0 = 永不过期
  show_spinner: true                       # 是否显示加载动画
```

### 字段说明

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `paths.raw_data` | str | `data/raw/sales.csv` | 默认数据文件路径 |
| `paths.processed_dir` | str | `data/processed` | 清洗后 CSV 保存目录 |
| `paths.charts_dir` | str | `output/charts` | 图表文件保存目录 |
| `paths.reports_dir` | str | `output/reports` | 报告输出目录 |
| `ui.page_title` | str | `跨境电商销售数据分析平台` | 浏览器标签页标题 |
| `ui.page_icon` | str | `📊` | 浏览器标签页图标 |
| `ui.layout` | str | `wide` | Streamlit 布局模式 |
| `ui.sidebar_title` | str | `导航` | 侧边栏标题文字 |
| `ui.default_page` | str | `概览` | 启动默认页面 |
| `charts.figure_size` | list | `[12, 6]` | Matplotlib figsize |
| `charts.dpi` | int | `120` | 图表输出 DPI |
| `charts.color_palette` | str | `tab10` | 图表默认配色 |
| `charts.font_family` | str | `Microsoft YaHei` | 图表首选中文字体 |
| `charts.fallback_font` | str | `SimHei` | 备选中文字体 |
| `charts.top_n_default` | int | `10` | 排行默认显示数量 |
| `filters.date_range` | null | `null` | 默认不筛选日期 |
| `filters.countries` | list | `[]` | 默认不筛选国家 |
| `filters.date_format` | str | `%Y-%m-%d` | 日期格式化字符串 |
| `cache.ttl_seconds` | int | `3600` | Streamlit 缓存过期秒数 |
| `cache.show_spinner` | bool | `true` | 计算时是否显示 spinner |

## 3. 加载流程

```
app.py 启动
    │
    ▼
load_config("config.yaml")
    │
    ├─ config.yaml 存在 ──→ 解析 YAML → 校验必填字段 → 返回 dict
    │
    └─ config.yaml 不存在 ──→ 打印警告 → 返回硬编码默认值（见第 5 节）
```

**config.py 实现要点：**
- `load_config()` 是唯一公共接口
- 内部用 `_validate_config()` 私有函数校验 schema
- 校验不通过 → 报错并终止（`st.error` + `st.stop()`），不静默降级
- 校验通过 → 返回 dict，调用方直接用 `cfg["paths"]["raw_data"]` 取值

## 4. Schema 校验规则

```python
REQUIRED_KEYS = ["paths", "ui", "charts", "filters", "cache"]

# 校验规则（按顺序）
# 1. 根节点必须是 dict
# 2. 5 个必填 top-level key 必须存在
# 3. paths.raw_data、ui.page_title、charts.font_family 必须为非空字符串
# 4. charts.figure_size 必须为 [int, int]
# 5. charts.top_n_default 必须为 1-50 之间的整数
# 6. filters.countries 必须为 list（可为空）
# 7. cache.ttl_seconds 必须为 >= 0 的整数
```

校验失败时给出精确错误信息，例如：
```
Config 校验失败: charts.top_n_default 应为 1–50 的整数，当前值为 0
```

## 5. 兜底默认值

当 `config.yaml` 文件不存在时（如首次克隆项目），`load_config()` 返回内置默认值：

```python
_DEFAULT_CONFIG = {
    "paths": {
        "raw_data": "data/raw/sales.csv",
        "processed_dir": "data/processed",
        "charts_dir": "output/charts",
        "reports_dir": "output/reports",
    },
    "ui": {
        "page_title": "跨境电商销售数据分析平台",
        "page_icon": "📊",
        "layout": "wide",
        "sidebar_title": "导航",
        "default_page": "概览",
    },
    "charts": {
        "figure_size": [12, 6],
        "dpi": 120,
        "color_palette": "tab10",
        "font_family": "Microsoft YaHei",
        "fallback_font": "SimHei",
        "top_n_default": 10,
    },
    "filters": {
        "date_range": None,
        "countries": [],
        "date_format": "%Y-%m-%d",
    },
    "cache": {
        "ttl_seconds": 3600,
        "show_spinner": True,
    },
}
```

**原则：默认值与 `config.yaml` 模板保持一致**，避免两套不同行为。

## 6. V3 扩展预留

V3 新增 AI 功能时，只需在 `config.yaml` 中追加节点：

```yaml
# V3 扩展（当前不实现，仅预留 schema）
ai:
  provider: "anthropic"                  # anthropic | openai
  model: "claude-sonnet-4-6"
  api_key_env: "ANTHROPIC_API_KEY"       # 从环境变量读取
  max_tokens: 2000
  language: "en"                         # 报告语言

export:
  pdf_enabled: false                     # PDF 导出开关
  email_enabled: false                   # 邮件发送开关
```

V2 的 `_validate_config()` 只校验 5 个必填 key，遇到未知 key（如 `ai`）忽略不报错，确保向后兼容。

## 7. 不做的优化（Sprint 2.1 范围外）

- **多环境配置**（dev/staging/prod）— 单人项目不需要
- **Config 热重载**（修改 YAML 自动刷新）— 重启 Streamlit 够用了
- **.env 覆盖 YAML** — 没有需要加密的敏感值，暂时不需要
- **命令行参数覆盖 Config** — 所有入口统一，避免碎片化
