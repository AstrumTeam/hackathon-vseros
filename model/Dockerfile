FROM python:3.9.6

RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get install cmake

COPY requirements.txt .
# Установка зависимостей (минимизируем вес образа за счёт очистки кеша pip)
RUN pip install --no-cache-dir --default-timeout=600 -r requirements.txt
# Копируем код проекта в рабочую директорию контейнера
COPY . .
# Открываем порт 8000 для доступа к FastAPI приложению
EXPOSE 8000
# Запуск приложения с помощью uvicorn
CMD ["uvicorn", "controller:app", "--host", "0.0.0.0", "--port", "8000"]