# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.10
FROM python:3.10

# Встановимо змінну середовища
ENV APP_HOME=/app

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

# Спочатку копіюємо requirements.txt та встановлюємо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопіюємо інші файли в робочу директорію контейнера
COPY . .

# Позначимо порт, де працює застосунок всередині контейнера
EXPOSE 3000

# Запустимо наш застосунок всередині контейнера
ENTRYPOINT ["python", "main.py"]