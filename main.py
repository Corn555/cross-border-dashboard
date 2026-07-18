"""
入口：CLI 模式 — 一键运行完整数据分析流程。

职责：
  1. 初始化 Logger
  2. 加载 Config
  3. 调用 Pipeline
  4. 统一异常处理
  5. 输出完成信息

注意：main.py 不包含任何业务逻辑，所有流程编排在 src/pipeline/ 中。
"""
import sys

from src.config import (
    CHARTS_OUTPUT_DIR,
    PROCESSED_DATA_PATH,
    RAW_DATA_PATH,
    REPORT_OUTPUT_PATH,
    VERSION,
)
from src.exceptions import ProjectError
from src.logger import get_logger, setup_logging
from src.pipeline import run_pipeline

logger = get_logger(__name__)


def main():
    """程序入口 — 初始化基础设施，启动 Pipeline。"""
    logger.info("Program started (v%s)", VERSION)

    try:
        result = run_pipeline(
            raw_data_path=RAW_DATA_PATH,
            processed_data_path=PROCESSED_DATA_PATH,
            charts_output_dir=CHARTS_OUTPUT_DIR,
            report_output_path=REPORT_OUTPUT_PATH,
        )
    except ProjectError:
        logger.exception("流程执行失败")
        sys.exit(1)

    print("=" * 56)
    print("  全部分析流程完成！")
    print(f"  报告位置: {result.report_path}")
    print("=" * 56 + "\n")
    logger.info("Program finished")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    setup_logging()
    main()
