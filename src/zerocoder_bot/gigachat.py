import logging

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

from .knowledge import COURSES_INFO, FAQ_INFO, ZEROCODER_INFO
from .prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

MODEL = "GigaChat-2-Max"
GIGACHAT_BASE_URL = "https://api.giga.chat/v1"
MAX_CONTEXT_MESSAGES = 20
LAST_N_MESSAGES = 10

FALLBACK_MESSAGE = (
    "Извините, произошла ошибка при обработке вашего запроса. "
    "Пожалуйста, попробуйте позже или свяжитесь с нами по телефону +7 (939) 328-38-12"
)


class SupportAssistant:
    """ИИ-консультант на базе GigaChat с историей диалогов."""

    def __init__(self, credentials: str, scope: str = "GIGACHAT_API_PERS"):
        self._client = GigaChat(
            base_url=GIGACHAT_BASE_URL,
            credentials=credentials,
            scope=scope,
            verify_ssl_certs=False,
        )
        self._sessions: dict[int, list[dict[str, str]]] = {}

    def get_response(self, user_id: int, user_message: str) -> str:
        """Получить ответ ассистента с учётом контекста беседы."""
        if user_id not in self._sessions:
            self._sessions[user_id] = []
        self._sessions[user_id].append({"role": "user", "content": user_message})

        knowledge = f"{ZEROCODER_INFO}\n{COURSES_INFO}\n{FAQ_INFO}"
        messages = [
            Messages(
                role=MessagesRole.SYSTEM,
                content=f"{SYSTEM_PROMPT}\n\nБаза знаний:\n{knowledge}",
            )
        ]
        for msg in self._sessions[user_id][-LAST_N_MESSAGES:]:
            role = (
                MessagesRole.USER
                if msg["role"] == "user"
                else MessagesRole.ASSISTANT
            )
            messages.append(Messages(role=role, content=msg["content"]))

        try:
            logger.info("Calling GigaChat API for user %s...", user_id)
            chat = Chat(model=MODEL, messages=messages)
            response = self._client.chat(chat)
            assistant_message = response.choices[0].message.content
            logger.info("GigaChat response: %s...", assistant_message[:100])

            self._sessions[user_id].append(
                {"role": "assistant", "content": assistant_message}
            )
            if len(self._sessions[user_id]) > MAX_CONTEXT_MESSAGES:
                self._sessions[user_id] = self._sessions[user_id][-MAX_CONTEXT_MESSAGES:]
            return assistant_message
        except Exception as exc:
            logger.error("GigaChat API error: %s", exc)
            return FALLBACK_MESSAGE
