# Task Tracker

**Task Tracker** — асинхронный бэкенд для трекера задач на микросервисной архитектуре: FastAPI-шлюз общается с независимыми доменными сервисами через RabbitMQ (RPC), у каждого сервиса своя схема PostgreSQL, real-time обновления идут через WebSocket + Redis pub/sub.

Проект — учебный (pet-project), но спроектирован по паттернам production-систем: RPC вместо REST между сервисами, event-driven обновления, централизованные контракты, трассировка и метрики из коробки.

---

## Содержание

- [Архитектура](#архитектура)
- [Сервисы](#сервисы)
- [Технологический стек](#технологический-стек)
- [Быстрый старт](#быстрый-старт)
- [Структура репозитория](#структура-репозитория)
- [Observability](#observability)
- [Тестирование](#тестирование)
- [Roadmap](#roadmap)

---

## Архитектура

Gateway — единственная точка входа с публичным HTTP/WebSocket API. Все запросы к доменным сервисам (user, task, category, tag, comment, attachment, chat) идут через RabbitMQ как RPC-вызовы. У каждого сервиса своя схема PostgreSQL. chat_service дополнительно использует Redis pub/sub для рассылки сообщений между воркерами и последующей доставки клиенту через WebSocket в gateway.

Каждый доменный сервис — это отдельный consumer, слушающий свою очередь в RabbitMQ. Gateway не знает о внутренней реализации сервисов, только о контрактах (`shared/contracts`), которые описывают запрос/ответ для каждой RPC-команды.

## Сервисы

| Сервис | Ответственность |
|---|---|
| **gateway** | Единая точка входа: HTTP API, JWT-аутентификация (RS256), проксирование запросов в очереди как RPC, WebSocket для real-time |
| **user_service** | Регистрация, вход, refresh-токены, профиль пользователя |
| **task_service** | CRUD задач, фильтрация, пагинация, привязка категорий/тегов |
| **category_service** | Категории задач |
| **tag_service** | Теги задач (уникальны в рамках пользователя) |
| **comment_service** | Комментарии к задачам |
| **attachment_service** | Загрузка и хранение вложений в S3 |
| **chat_service** | Чат по задачам в реальном времени (WebSocket + Redis pub/sub, персистентность сообщений) |

## Технологический стек

- **API:** FastAPI, Pydantic v2
- **Данные:** PostgreSQL (asyncpg + SQLAlchemy 2.0 + Alembic), схема на сервис
- **Очереди:** RabbitMQ (aio-pika) — RPC между gateway и сервисами
- **Real-time:** WebSocket + Redis pub/sub (multi-worker broadcast)
- **Auth:** JWT RS256, refresh-токены в Redis
- **Хранилище файлов:** S3-совместимое (aiobotocore)
- **Наблюдаемость:** OpenTelemetry, Jaeger (трейсинг), Prometheus + Grafana (метрики), Loki + Promtail (логи)
- **Инфраструктура:** Docker Compose, Poetry, Ruff

## Быстрый старт

```bash
# 1. Поднять инфраструктуру и все сервисы
docker-compose up -d

# 2. Применить миграции (выполняется автоматически через migrate_* сервисы,
#    либо вручную для конкретного сервиса)
docker-compose run --rm migrate_user
docker-compose run --rm migrate_task

# 3. Сгенерировать ключи JWT (если ещё нет)
mkdir -p keys
openssl genrsa -out keys/private.pem 2048
openssl rsa -in keys/private.pem -pubout -out keys/public.pem

# 4. Проверить, что всё поднялось
curl http://localhost:8000/api/v1/health
```

Локальная разработка одного сервиса (без Docker):

```bash
cd user_service
poetry install
poetry run alembic upgrade head
poetry run uvicorn user_service.main:app --reload
```

## Структура репозитория

```
.
├── gateway/            # FastAPI-шлюз, единственный сервис с публичным HTTP API
├── user_service/        # auth + профиль пользователя
├── task_service/        # задачи
├── category_service/     # категории
├── tag_service/          # теги
├── comment_service/      # комментарии
├── attachment_service/   # вложения (S3)
├── chat_service/         # чат (WebSocket + Redis)
├── shared/               # общий пакет: контракты RPC, брокер, база моделей, логирование, метрики
├── docker-compose.yml
├── prometheus.yml
└── promtail-config.yaml
```

Каждый сервис (кроме gateway) имеет одинаковую внутреннюю структуру:

```
<service>/
├── <service>/
│   ├── models/       # SQLAlchemy-модели (только для Alembic)
│   ├── repository/    # доступ к данным
│   ├── services/       # бизнес-логика
│   ├── broker/         # обработчики RPC-команд (consumer)
│   ├── schemas/        # Pydantic-схемы
│   ├── exceptions/     # доменные исключения
│   └── core/            # конфиг, подключение к БД
├── migrations/          # Alembic
└── consumer_main.py     # точка входа consumer'а
```

## Observability

- **Трейсинг:** Jaeger UI — `http://localhost:16686`
- **Метрики:** Prometheus — `http://localhost:9090`, Grafana — `http://localhost:3000`
- **Логи:** Loki + Promtail, агрегация логов со всех контейнеров
- Все запросы через gateway помечаются `X-Request-ID` и трассируются сквозь очередь RPC до сервиса-обработчика

## Тестирование

Сейчас в активной работе: подключение pytest / pytest-asyncio / pytest-cov по всем сервисам с целью **80% покрытия**. Приоритет — бизнес-логика (`services/`) и репозитории, затем брокер-обработчики, в последнюю очередь — `chat_service` из-за сложности WebSocket + Redis.

```bash
cd <service>
poetry run pytest --cov=<service> --cov-report=term-missing
```

## Roadmap

- [ ] Тесты, 80% покрытия по всем сервисам
- [ ] Rate limiting в gateway
