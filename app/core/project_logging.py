import logging
import logging.config as log_conf
import yaml
from pathlib import Path
from config.settings import settings


def setup_logging():
    """加载并应用日志配置"""
    # 确保生产环境日志目录存在
    if settings.ENVIRONMENT == "prod":
        settings.LOG_DIR.mkdir(parents=True, exist_ok=True)

    # 读取日志配置文件
    config_path = settings.LOGGING_CONFIG_PATH
    if not config_path.exists():
        raise FileNotFoundError(f"日志配置文件不存在: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        logging_config = yaml.safe_load(f)

    # 替换生产环境日志文件路径（避免硬编码在 yaml 中）
    if settings.ENVIRONMENT == "prod":
        for handler_name, handler_config in logging_config.get("handlers", {}).items():
            if "filename" in handler_config:
                # 原路径可能是 "./logs/app.log"，替换为绝对路径
                filename = Path(handler_config["filename"]).name
                handler_config["filename"] = str(settings.LOG_DIR / filename)

    # 应用日志配置
    log_conf.dictConfig(logging_config)


# 初始化日志
setup_logging()

# 项目全局 logger
logger = logging.getLogger("app")