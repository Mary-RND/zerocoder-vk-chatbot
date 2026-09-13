"""Хранилище истории диалогов с ограничением размера."""

from collections import defaultdict, deque


class SessionMemory:
    """Держит последние N сообщений для каждого пользователя."""

    def __init__(self, max_messages: int = 20):
        self._max = max_messages
        self._sessions: dict[int, deque[dict[str, str]]] = defaultdict(deque)

    def append(self, user_id: int, role: str, content: str) -> None:
        """Добавить сообщение в историю, вытесняя самые старые."""
        session = self._sessions[user_id]
        session.append({"role": role, "content": content})
        while len(session) > self._max:
            session.popleft()

    def get(self, user_id: int, last_n: int | None = None) -> list[dict[str, str]]:
        """Вернуть историю (последние last_n сообщений или всю)."""
        session = self._sessions[user_id]
        if last_n is None:
            return list(session)
        return list(session)[-last_n:]

    def clear(self, user_id: int) -> None:
        """Сбросить историю пользователя."""
        self._sessions.pop(user_id, None)

    def __len__(self) -> int:
        return sum(len(session) for session in self._sessions.values())