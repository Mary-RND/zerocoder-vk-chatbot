import logging

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from .config import load_settings
from .gigachat import SupportAssistant

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


FALLBACK_ANSWER = (
    "Извините, произошла ошибка при обработке вашего запроса. "
    "Пожалуйста, попробуйте позже или свяжитесь с нами по телефону +7 (939) 328-38-12"
)


def main() -> None:
    settings = load_settings()
    assistant = SupportAssistant(
        settings.gigachat_credentials, settings.gigachat_scope
    )

    try:
        vk_session = VkApi(token=settings.vk_token)
        longpoll = VkBotLongPoll(vk_session, group_id=settings.vk_group_id)
        logger.info("Bot started successfully!")
    except Exception as exc:
        logger.error("Failed to initialize VK API: %s", exc)
        raise

    for event in longpoll.listen():
        if event.type != VkBotEventType.MESSAGE_NEW:
            continue

        message = event.obj.message
        user_id = message["from_id"]
        peer_id = message["peer_id"]
        text = message.get("text", "")

        logger.info("Message from user %s (peer_id=%s): %s", user_id, peer_id, text)
        if not text.strip():
            continue

        response = assistant.get_response(user_id, text)
        if not response:
            response = FALLBACK_ANSWER

        vk_session.method(
            "messages.send",
            {
                "peer_id": peer_id,
                "message": response,
                "random_id": 0,
            },
        )
        logger.info("Response sent to peer_id=%s", peer_id)


if __name__ == "__main__":
    main()