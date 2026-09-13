# Развёртывание

Бот работает по схеме Long Poll — не требует публичного webhook,
поэтому его можно запускать на любом хосте с доступом в интернет.

## Вариант 1. Локальный запуск (systemd / фоновый процесс)

```bash
pip install -e .
cp .env.example .env
# заполните .env реальными значениями
zerocoder-bot
```

## Вариант 2. Docker

Базовый `Dockerfile:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["zerocoder-bot"]
```

Сборка и запуск:

```bash
docker build -t zerocoder-bot .
docker run -d --env-file .env zerocoder-bot
```

## Мониторинг

- Логи пишутся в stdout (`logging.INFO`).
- Для отправки ошибок в Telegram/почту добавьте отдельный logging handler.

## Масштабирование

При росте нагрузки переносите хранилище диалогов в Redis:

```python
# пример: сессия в Redis
import redis
r = redis.Redis()
r.lpush(f"session:{user_id}", message)
```
