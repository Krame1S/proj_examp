FROM python:3.12-slim

WORKDIR /app

COPY shared/ /app/shared/

COPY gateway/pyproject.toml gateway/poetry.lock ./

RUN pip install poetry==1.8.3 --no-cache-dir --only-binary :all: && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --without dev

COPY gateway/ .
COPY keys/ /app/keys/

ENV PYTHONPATH="/app:/app/shared/src"

RUN useradd --create-home --shell /bin/false appuser && chown -R appuser:appuser /app
USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
