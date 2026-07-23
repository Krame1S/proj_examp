FROM python:3.12-slim

WORKDIR /app

COPY shared/ /app/shared/

COPY user_service/pyproject.toml user_service/poetry.lock* ./

RUN pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --without dev

COPY user_service/ .

COPY keys/ /app/keys/

ENV PYTHONPATH="/app:/app/shared/src"

RUN useradd --create-home --shell /bin/false appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "consumer_main.py"]
