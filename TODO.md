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

## In Progress

### File Attachments

- [ ] Create attachment model and migration
- [ ] Implement file upload to S3
- [ ] Store file metadata in DB (key, filename, content_type, size)
- [ ] Return public URL via S3_PUBLIC_URL
- [ ] Add delete attachment endpoint

## Planned

- [ ] Add task search
- [ ] Write unit tests (target 80% coverage)
