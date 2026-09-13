# Zerocoder VK Chatbot 🎓

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![vk-api](https://img.shields.io/badge/vk--api-11.10%2B-green)
![gigachat](https://img.shields.io/badge/gigachat-0.2.3%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Чат-бот для сообщества ВКонтакте, который консультирует абитуриентов университета **Zerocoder** по программам обучения, курсам, стоимости и формам обучения.

Бот работает как ИИ-ассистент **«Алина»**: отвечает на вопросы из базы знаний, помогает выбрать подходящее направление (промпт-инжиниринг, вайб-кодинг, ИИ-консалтинг и др.) и при необходимости направляет к менеджерам.

Генерация ответов выполняется через **GigaChat API** (Sber) с учётом контекста диалога (до 20 последних сообщений на пользователя).

---

## Возможности

- 💬 Ответы на вопросы о курсах и программах Zerocoder на основе базы знаний
- 🧠 Контекст диалога — бот помнит историю переписки каждого пользователя
- 🎯 Помощь в выборе направления обучения и деликатная передача контактов менеджеру
- 🛡️ Graceful-обработка ошибок GigaChat (без падения бота)
- 🔀 Ветвление: проверка is_current для идемпотентной отправки сообщений
- 📝 Логирование всех сообщений и ответов

## Стек

| Компонент | Технология |
|-----------|------------|
| Платформа | ВКонтакте (vk_api + Bot Long Poll)` |
| ИИ-генерация | GigaChat API (`GigaChat-2-Max`) |
| Язык | Python 3.10+ |
| Конфигурация | .env + python-dotenv |

## Структура проекта

```
.
├── src/
│   └── zerocoder_bot/
│       ├── __init__.py          # пакет
│       ├── config.py            # загрузка и валидация конфигурации
│       ├── bot.py               # точка входа: VK Long Poll + рассылка ответов
│       ├── gigachat.py          # интеграция с GigaChat, управление диалогами
│       ├── knowledge.py         # база знаний (курсы, контакты, FAQ)
│       └── prompts.py           # системный промпт ассистента «Алина»
├── scripts/
│   └── debug.py                 # диагностика VK Long Poll событий
├── tests/
│   └── test_knowledge.py        # юнит-тесты базы знаний
├── docs/
│   └── architecture.md          # архитектурная схема
├── .env.example                 # шаблон переменных окружения
├── .gitignore
├── pyproject.toml               # упаковка и зависимости
├── requirements.txt             # зависимости проекта
├── requirements-dev.txt         # зависимости для разработки
└── LICENSE
```

## Установка и запуск

### 1. Клонирование

```bash
git clone https://github.com/Mary-RND/zerocoder-vk-chatbot.git
cd zerocoder-vk-chatbot
```

### 2. Установка зависимостей

```bash
pip install -e .
```

Для разработки (включая тесты):

```bash
pip install -e ".[dev]"
```

### 3. Настройка окружения

```bash
cp .env.example .env
```

Заполните `.env` своими ключами (см. ниже).

### 4. Запуск

```bash
zerocoder-bot
```

или

```bash
python -m zerocoder_bot.bot
```

Диагностика событий VK Long Poll:

```bash
python -m scripts.debug
```

## Переменные окружения

```dotenv
# ===== GIGACHAT API =====
GIGACHAT_CREDENTIALS=your_gigachat_authorization_key_here
GIGACHAT_SCOPE=GIGACHAT_API_PERS

# ===== VK API =====
VK_TOKEN=your_vk_community_token_here
VK_GROUP_ID=your_group_id_here
```

| Переменная | Описание |
|------------|----------|
| `GIGACHAT_CREDENTIALS` | Ключ авторизации GigaChat API из личного кабинета (https://developers.sber.ru/) |
| `GIGACHAT_SCOPE` | Область API: `GIGACHAT_API_PERS` (физлица) или `GIGACHAT_API_B2B` (бизнес) |
| `VK_TOKEN` | Ключ доступа сообщества ВКонтакте (Управление → Работа с API) |
| `VK_GROUP_ID` | ID сообщества без знака «минус» |

### Как получить токен VK

1. Перейдите в **Управление сообществом**
2. Откройте **Управление → Работа с API**
3. Создайте ключ доступа с правами на сообщения
4. Скопируйте токен

### Как получить ключ GigaChat

1. Перейдите в личный кабинет (https://developers.sber.ru/)
2. Откройте проект **GigaChat API**
3. Перейдите в **Настройки API**
4. Нажмите **«Получить ключ»**
5. Скопируйте ключ авторизации

## Архитектура

```
┌────────────┐    Long Poll    ┌──────────────┐    REST    ┌────────────┐
│   VK       │ ──────────────▶ │      Bot     │ ─────────▶ │  GigaChat  │
│ community  │ ◀────────────── │ (zerocoder_  │ ◀───────── │    API     │
└────────────┘   messages.send │  bot)        │            └────────────┘
                               └──────────────┘
                                      │
                                      ▼
                               ┌──────────────┐
                               │  knowledge.py │
                               │  (база знаний)│
                               └──────────────┘
```

Подробности: [docs/architecture.md](docs/architecture.md).

## Тестирование

```bash
pytest -v
```

## Модель веток

- `main` — стабильные релизы
- `develop` — интеграционная ветка (CI, документация)
- `feature/*` — разработка новых функций

## Лицензия

MIT — см. [LICENSE](LICENSE).

## Контакты

- 📞 Телефон: +7 (939) 328-38-12
- 📧 Email: care@zerocoder.ru
- 📍 Адрес: г. Москва, ул. Большая Новодмитровская 23, этаж 2, каб. 46
