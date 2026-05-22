FROM python:3.12-slim

WORKDIR /app

# shared копируется через build context корня
COPY shared/ /app/shared/

COPY user_service/pyproject.toml user_service/poetry.lock* ./

RUN pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --without dev

COPY user_service/ .

# keys нужны для JWT — монтируем из корня проекта
COPY keys/ /app/keys/

ENV PYTHONPATH="/app/shared/src"

# user_service — это RabbitMQ consumer, не HTTP-сервер
CMD ["python", "consumer_main.py"]