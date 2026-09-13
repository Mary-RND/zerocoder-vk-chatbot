import os
import sys
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    vk_token: str
    vk_group_id: int
    gigachat_credentials: str
    gigachat_scope: str = "GIGACHAT_API_PERS"


def load_settings() -> Settings:
    """Загрузить и провалидировать настройки из переменных окружения."""
    load_dotenv()

    vk_token = os.getenv("VK_TOKEN", "")
    vk_group_id = os.getenv("VK_GROUP_ID", "")
    gigachat_credentials = os.getenv("GIGACHAT_CREDENTIALS", "")
    gigachat_scope = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")

    missing = [
        name
        for name, value in (
            ("VK_TOKEN", vk_token),
            ("VK_GROUP_ID", vk_group_id),
            ("GIGACHAT_CREDENTIALS", gigachat_credentials),
        )
        if not value
    ]
    if missing:
        print(
            f"Ошибка: не заданы переменные окружения: {', '.join(missing)}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        group_id = int(vk_group_id)
    except ValueError:
        print("Ошибка: VK_GROUP_ID должен быть числом", file=sys.stderr)
        sys.exit(1)

    return Settings(
        vk_token=vk_token,
        vk_group_id=group_id,
        gigachat_credentials=gigachat_credentials,
        gigachat_scope=gigachat_scope,
    )
