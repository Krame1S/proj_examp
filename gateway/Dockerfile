FROM python:3.12-slim

WORKDIR /app

# shared копируется через build context корня (context: . в docker-compose)
COPY shared/ /app/shared/

COPY gateway/pyproject.toml gateway/poetry.lock* ./

RUN pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --without dev

COPY gateway/ .
COPY keys/ /app/keys/

ENV PYTHONPATH="/app:/app/shared/src"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]