FROM python:3.11-slim

# Установим системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем и ставим зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .
COPY userbot_session.session /app/app/bot/userbot_session.session
# Запуск бота
CMD ["python", "-m", "app.bot.Bot"]
