"""
模块：统一异常体系
职责：定义项目所有自定义异常类，按 Pipeline 阶段划分。

用法：
    from src.exceptions import DataLoadError
    raise DataLoadError("文件不存在: data/raw/sales.csv")
"""


class ProjectError(Exception):
    """项目所有自定义异常的基类。"""


class DataLoadError(ProjectError):
    """数据加载阶段失败 — 文件不存在、编码错误、格式异常。"""


class DataCleanError(ProjectError):
    """数据清洗阶段失败 — 空 DataFrame、列缺失、类型转换异常。"""


class AnalysisError(ProjectError):
    """数据分析阶段失败 — 计算异常、数据不足以完成分析。"""


class VisualizationError(ProjectError):
    """图表生成阶段失败 — 字体缺失、磁盘空间不足、数据格式不匹配。"""


class ReportGenerationError(ProjectError):
    """报告生成阶段失败 — 模板错误、文件写入失败。"""
