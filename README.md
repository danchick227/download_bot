# Download Bot

Telegram-бот для скачивания видео с YouTube и отправки файла в чат.

## Требования

- Python 3.14+
- Docker и Docker Compose (опционально, для запуска в контейнере)
- Токен Telegram-бота

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/danchick227/download_bot.git
   cd download_bot
   ```

2. Создайте виртуальное окружение и установите зависимости:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -U pip
   pip install -e .
   ```

   Или, если используете `uv`:

   ```bash
   uv sync
   ```

3. Настройте переменные окружения:

   ```bash
   cp .env.example .env
   ```

   Затем откройте `.env` и укажите токен бота:

   ```env
   BOT_TOKEN=your_bot_token_here
   ```

## Запуск локально

После настройки `.env` запустите бота:

```bash
source .venv/bin/activate
python -m download_bot.main
```

## Запуск через Docker

1. Убедитесь, что в корне есть файл `.env` с `BOT_TOKEN`.
2. Запустите контейнер:

   ```bash
   docker compose up --build -d
   ```

3. Посмотреть логи:

   ```bash
   docker compose logs -f bot
   ```

4. Остановить:

   ```bash
   docker compose down
   ```

## Как работает бот

- Пользователь отправляет ссылку на YouTube-видео.
- Бот проверяет, что это корректная ссылка.
- Скачивает файл через `yt-dlp` во временную директорию.
- Отправляет готовое видео обратно в Telegram.

## Структура проекта

```text
.
├── .env.example
├── docker-compose.yml
├── dockerfile
├── README.md
├── pyproject.toml
├── src/
│   └── download_bot/
│       ├── config.py
│       ├── main.py
│       ├── handlers/
│       └── services/
└── uv.lock
```
