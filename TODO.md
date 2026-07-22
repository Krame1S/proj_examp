# TODO

## Completed

- [x] Add task_count field to categories with CTE query for user categories
- [x] Add category filtering with validation and repository method for tasks
- [x] Add category_name to task queries with LEFT JOIN
- [x] Return category_name in create_task using CTE
- [x] Fix Body() missing parentheses in sign_up endpoint
- [x] Add upper bound validation to all Path and Query int parameters

### Tags

- [x] Create tag model and migration
- [x] Create tag schema and CRUD
- [x] Fix tag uniqueness to be per-user (UNIQUE(name, created_by))
- [x] Add tags to all task queries via ARRAY_AGG
- [x] Implement set_tags_on_task with CTE diff pattern
- [x] Integrate tag assignment in create_task and patch_task
- [x] Add tags field to TaskOut schema
- [x] Add GetTaskResponse schema with has_more pagination
- [x] Remove skip-based pagination, switch to limit+1 pattern
- [x] Implement filter tasks by tags with AND logic

### Comments

- [x] Create comment model and migration
- [x] Create comment schema, repository, service and CRUD endpoints
- [x] Nest comments under /tasks/{task_id}/comments

### File Attachments

- [x] Create attachment model and migration
- [x] Implement file upload to S3
- [x] Store file metadata in DB (key, filename, content_type, size)
- [x] Return public URL via S3_PUBLIC_URL
- [x] Add delete attachment endpoint

### Microservices Migration

- [x] Set up gateway as standalone service with RabbitMQ RPC proxy
- [x] Set up user_service as standalone RabbitMQ consumer
- [x] Set up shared library (broker queues, exchanges, exceptions)
- [x] Implement sign_up, sign_in, refresh via RabbitMQ RPC
- [x] Implement JWT verification in gateway (RS256, public key only)
- [x] Implement user profile endpoints (GET /users/me, PUT /users/me, DELETE /users/me)
- [x] Configure Docker Compose with healthchecks and migration service
- [x] Set up Alembic autogenerate with SQLAlchemy models in user_service

## In Progress

### task_service

- [ ] Set up task_service as standalone RabbitMQ consumer
- [ ] Migrate tasks (CRUD, filtering, pagination, tags)
- [ ] Migrate categories (CRUD, task_count)
- [ ] Migrate tags (CRUD, per-user uniqueness)
- [ ] Migrate comments (CRUD, nested under tasks)
- [ ] Add task_service to Docker Compose

## Planned

- [ ] Add task search
- [ ] Write unit tests (target 80% coverage)
- [ ] Add rate limiting in gateway
- [ ] Add request_id tracing across services
