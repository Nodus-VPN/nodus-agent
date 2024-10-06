# Используем официальный базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Создаем папки logs и abi, если они не будут скопированы
RUN mkdir -p /app/logs /app/abi

# Копируем содержимое папок abi и logs
COPY ./abi /app/abi
COPY ./logs /app/logs

# Запускаем ваше приложение
CMD ["python", "EventListener.py"]
