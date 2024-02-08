FROM python:3.11

# Сборка зависимостей
ARG BUILD_DEPS="curl"
RUN apt-get update && apt-get install -y $BUILD_DEPS

# Установка poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
ENV PATH="${PATH}:/etc/poetry/bin"

# Инициализация проекта
WORKDIR /app

# PYTHONUNBUFFERED отвечает за отключение буферизации вывода (output).
# То есть непустое значение данной переменной среды гарантирует,
# что мы можем видеть выходные данные нашего приложения в режиме реального времени.
ENV PYTHONUNBUFFERED 1
#PYTHONDONTWRITEBYTECODE означает, что Python не будет пытаться создавать файлы .pyc.
ENV PYTHONDONTWRITEBYTECODE 1

# Установка библиотек
COPY pyproject.toml /app

RUN poetry config virtualenvs.create false
RUN poetry install --only main

# весь проект копируется внутрь контейнера, в WORKDIR.
COPY . .

# даем доступ для запуска docker скриптов
RUN chmod a+x /app/docker/app.sh