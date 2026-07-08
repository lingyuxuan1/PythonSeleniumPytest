#from __future__ import annotations

import os
from dataclasses import dataclass
#from pathlib import Path


def _env(name: str, default: str) -> str:
    """读取字符串类型环境变量，未配置时返回默认值。"""
    v = os.getenv(name)
    return default if v is None or v == "" else v


def _env_int(name: str, default: int) -> int:
    """读取整数类型环境变量，未配置时返回默认值。"""
    v = os.getenv(name)
    if v is None or v == "":
        return default
    return int(v)


def _env_bool(name: str, default: bool) -> bool:
    """读取布尔类型环境变量，未配置时返回默认值。"""
    v = os.getenv(name)
    if v is None or v == "":
        return default
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    browser: str = _env("BROWSER", "edge").strip().lower()
    headless: bool = _env_bool("HEADLESS", True)
    base_url: str = _env("BASE_URL", "https://rag.yifatong.com")

    implicit_wait_seconds: int = _env_int("IMPLICIT_WAIT_SECONDS", 5)
    explicit_wait_seconds: int = _env_int("EXPLICIT_WAIT_SECONDS", 5)
    page_load_timeout_seconds: int = _env_int("PAGE_LOAD_TIMEOUT_SECONDS", 30)

    #artifacts_dir: Path = Path(_env("ARTIFACTS_DIR", "artifacts")).resolve()


settings = Settings()
