import logging
import json
from datetime import datetime
from typing import Any


class JsonFormatter(logging.Formatter):
    """自定义 JSON 日志格式化器（不依赖 pythonjsonlogger）"""

    def format(self, record: logging.LogRecord) -> str:
        # 基础日志字段
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),  # 时间戳（ISO格式）
            "level": record.levelname,  # 日志级别（INFO/ERROR等）
            "name": record.name,  # 日志器名称
            "module": record.module,  # 模块名
            "lineno": record.lineno,  # 行号
            "message": record.getMessage(),  # 日志消息
        }

        # 若有异常，添加堆栈信息
        if record.exc_info:
            log_data["exc_info"] = self.formatException(record.exc_info)

        # 转换为 JSON 字符串
        return json.dumps(log_data, ensure_ascii=False)