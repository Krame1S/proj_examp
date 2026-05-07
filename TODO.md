# TODO

## Completed

- [x] Add task_count field to categories with CTE query for user categories
- [x] Add category filtering with validation and repository method for tasks
- [x] Add category_name to task queries with LEFT JOIN
- [x] Return category_name in create_task using CTE

### Tags

- [x] Create tag model
- [x] Create tag migration
- [x] Create tag schema
- [x] Create CRUD for tags
- [x] Fix tag uniqueness to be per-user (UNIQUE(name, created_by))
- [x] Add tags to all task queries via ARRAY_AGG
- [x] Implement set_tags_on_task with CTE diff pattern
- [x] Integrate tag assignment in create_task and patch_task
- [x] Add tags field to TaskOut schema
- [x] Add GetTaskResponse schema with has_more pagination
- [x] Remove skip-based pagination, switch to limit+1 pattern
- [x] Fix Body() missing parentheses in sign_up endpoint

## In Progress

### Tags

- [ ] Add tag filtering to list tasks endpoint
- [ ] Implement filter by tags with AND logic

## Planned

- [ ] Add task search
- [ ] Add file attachments to tasks
- [ ] Add comments to tasks
- [ ] Write unit tests (target 80% coverage)
