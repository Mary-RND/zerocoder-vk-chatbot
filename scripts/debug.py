import logging

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from zerocoder_bot.config import load_settings

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    settings = load_settings()
    vk_session = VkApi(token=settings.vk_token)
    longpoll = VkBotLongPoll(vk_session, group_id=settings.vk_group_id)
    logger.info("Debug started! Listening for messages...")

    count = 0
    for event in longpoll.listen():
        count += 1
        logger.info("Event #%d: type=%s", count, event.type)
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.obj.message
            logger.info(
                "MESSAGE: from_id=%s, peer_id=%s, text=%s",
                msg.get("from_id"),
                msg.get("peer_id"),
                msg.get("text"),
            )
            logger.info("Full message object keys: %s", list(msg.keys()))
        if count >= 10:
            logger.info("Stopping after 10 events")
            break


if __name__ == "__main__":
    main()
