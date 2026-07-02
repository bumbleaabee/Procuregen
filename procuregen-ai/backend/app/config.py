"""
应用配置：从 .env 文件和环境变量读取参数，支持 Mock 降级。
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件（优先级高于系统环境变量）
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path, override=True)


class Settings:
    LLM_MODE = os.getenv("LLM_MODE", "mock")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    _base_dir = Path(__file__).resolve().parent.parent
    DATABASE_PATH = str(_base_dir / "procuregen.db")
    EXPORT_DIR = str(_base_dir.parent / "exports")
    TEMPLATE_DIR = str(_base_dir.parent / "templates")

    @classmethod
    def is_mock(cls) -> bool:
        return cls.LLM_MODE == "mock" or not cls.DEEPSEEK_API_KEY

    @classmethod
    def summary(cls) -> dict:
        return {
            "llm_mode": cls.LLM_MODE,
            "is_mock": cls.is_mock(),
            "model": cls.DEEPSEEK_MODEL if not cls.is_mock() else "mock",
        }


settings = Settings()
