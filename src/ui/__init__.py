"""src.ui — Streamlit 展示层组件。

每个页面模块导出 show() 函数，由 app.py 路由调用。
不包含任何业务逻辑，仅负责 Streamlit 渲染。
"""
from src.ui import about, analysis, charts, components, report, upload

__all__ = ["about", "analysis", "charts", "components", "report", "upload"]
