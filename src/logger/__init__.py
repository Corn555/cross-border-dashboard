"""
模块：src.logger
职责：统一日志系统 — 控制台 + 文件双输出。

用法：
    from src.logger import setup_logging, get_logger

    setup_logging()
    logger = get_logger(__name__)
    logger.info("Program started")
"""

from .logger import get_logger, setup_logging

__all__ = ["setup_logging", "get_logger"]
