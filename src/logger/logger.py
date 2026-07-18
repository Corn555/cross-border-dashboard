"""
模块：日志系统
职责：提供统一的日志记录能力，控制台 + 文件双输出。

用法：
    from src.logger import setup_logging, get_logger
    setup_logging()
    logger = get_logger(__name__)
    logger.info("操作完成")
"""
import logging
import os
from pathlib import Path


def setup_logging(
    log_dir: str = "logs",
    log_file: str = "app.log",
    level: int = logging.INFO,
) -> None:
    """
    初始化日志系统（仅在应用启动时调用一次）。

    配置 root logger 同时输出到控制台和日志文件。
    自动创建日志目录（如不存在）。重复调用不会添加重复 handler。

    Args:
        log_dir: 日志文件目录。
        log_file: 日志文件名。
        level: 日志级别阈值。
    """
    root = logging.getLogger()

    # 防止重复初始化（例如测试中多次调用）
    if root.handlers:
        return

    root.setLevel(level)

    # 创建日志目录
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # 日志格式：时间 [等级] 模块名: 内容
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-5s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台输出
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    root.addHandler(console)

    # 文件输出
    file_path = os.path.join(log_dir, log_file)
    file_handler = logging.FileHandler(file_path, encoding="utf-8")
    file_handler.setFormatter(fmt)
    root.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的 logger 实例。

    模块级用法：logger = get_logger(__name__)

    Args:
        name: logger 名称（通常传 __name__）。

    Returns:
        logging.Logger: 配置好的 logger 实例。
    """
    return logging.getLogger(name)
