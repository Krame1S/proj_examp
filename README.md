# Python Backend Template

FastAPI + asyncpg + Redis + JWT RS256 + S3 + Prometheus

## Quick Start

```bash
# 1. Install dependencies
poetry install

# 2. Start infrastructure
docker-compose up -d

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Generate JWT keys
mkdir -p keys
openssl genrsa -out keys/private.pem 2048
openssl rsa -in keys/private.pem -pubout -out keys/public.pem

# 5. Run migrations
alembic upgrade head

# 6. Start server
uvicorn main:app --reload
```

## Project Structure

```
src/
  api/          # Routes + DI (deps.py)
  core/         # Config + Security (JWT, passwords)
  db/           # asyncpg pool management
  models/       # SQLAlchemy models (Alembic only)
  schemas/      # Pydantic request/response models
  repository/   # Data access layer (raw SQL via asyncpg)
  service/      # Business logic
  middleware/    # Logging (correlation IDs) + Prometheus metrics
  utils/        # S3, logging setup
pg/             # Alembic migrations
tests/          # pytest-asyncio + httpx
```

## Key Patterns

- **DI via `Depends()`**: `get_db()` → `UserRepository(conn)` → `UserService(repo)` → route handler
- **asyncpg for queries**: Raw SQL in repositories, SQLAlchemy models only for Alembic
- **JWT RS256**: Asymmetric keys, refresh tokens stored in Redis (single-use)
- **Deep health check**: `GET /api/v1/health` verifies DB + Redis connectivity
- **S3 with retry**: tenacity exponential backoff on transient errors
- **Correlation IDs**: `X-Request-ID` header propagated through request lifecycle

## Commands

```bash
# Run tests
poetry run pytest

# Lint
poetry run ruff check src/ tests/

# Format
poetry run ruff format src/ tests/

# New migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```
