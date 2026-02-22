FROM python:3.12-slim

RUN pip install --no-cache-dir poetry==1.8.4

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "-w", "4"]
