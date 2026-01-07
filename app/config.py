from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os

# Корень проекта: папка на уровень выше app/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

# Загружаем именно этот файл
load_dotenv(ENV_PATH)

@dataclass(frozen=True)
class Config:
    bot_token: str

def load_config() -> Config:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError(f"BOT_TOKEN не найден в {ENV_PATH}")
    return Config(bot_token=token)
