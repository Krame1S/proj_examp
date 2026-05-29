FROM python:3.12-slim

WORKDIR /app

COPY shared/ /app/shared/

COPY tag_service/pyproject.toml tag_service/poetry.lock* ./

RUN pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --without dev

COPY tag_service/ .

ENV PYTHONPATH="/app:/app/shared/src"

CMD ["python", "consumer_main.py"]