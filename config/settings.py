from pydantic_settings import BaseSettings
from pydantic import Field, AnyUrl, ConfigDict
from pathlib import Path
from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class Settings(BaseSettings):
    # 基础配置
    PROJECT_ROOT: Path = Path(__file__).parent.parent


    # 从.env读取的核心变量（必须在.env中定义，否则报错）
    ENVIRONMENT: Environment = Field(default=Environment.DEVELOPMENT)
    DATABASE_URL: AnyUrl  # 自动验证URL格式
    API_KEY: str  # 敏感密钥

    # 从.env读取的可选变量（有默认值，.env中不定义则用默认值）
    PORT: int = 8000   # 服务端口
    LOG_LEVEL: str = "INFO"  # 日志级别

    # 其他业务相关配置（可结合环境动态调整）
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]  # 前端跨域地址

    # 日志配置文件路径（根据环境动态切换）
    @property
    def LOGGING_CONFIG_PATH(self) -> Path:
        if self.ENVIRONMENT == Environment.DEVELOPMENT:
            return self.PROJECT_ROOT / "config" / "logging_dev.yaml"
        else:
            return self.PROJECT_ROOT / "config" / "logging_prod.yaml"

    # 日志输出目录（生产环境用）
    LOG_DIR: Path = Field(default=PROJECT_ROOT / "logs")


    model_config = ConfigDict(  # 用 model_config 替代 class Config
        env_file=".env",
        case_sensitive=True,
        env_file_encoding="utf-8"
    )

    # 初始化时根据环境动态调整配置（可选）
    def __init__(self, **data):
        super().__init__(**data)
        # 开发环境自动开启DEBUG
        if self.ENVIRONMENT == Environment.DEVELOPMENT:
            self.DEBUG = True
            self.LOG_LEVEL = "DEBUG"  # 覆盖默认日志级别
        # 生产环境强化安全配置
        elif self.ENVIRONMENT == Environment.PRODUCTION:
            self.DEBUG = False
            self.LOG_LEVEL = "INFO"
            # # 生产环境API_KEY必须足够长（示例校验）
            # if len(self.API_KEY) < 16:
            #     raise ValueError("生产环境API_KEY长度不能少于16位")

settings = Settings()