# Tasks: MCP Server & Todo Tooling

**Input**: Design documents from `/specs/005-mcp-todo-tooling/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `tests/` at repository root
- Paths shown below assume `backend/src/` as the primary development focus for this feature.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [X] T001 Initialize Python environment and install dependencies (including MCP SDK, SQLModel) from `backend/requirements.txt`
- [X] T002 Configure environment variables for database connection and JWT secret from `backend/.env.example` to `backend/.env`
- [X] T003 Review and update `backend/Dockerfile` for deployment readiness
- [X] T004 Review and update `backend/alembic.ini` for database migrations configuration

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

### Database Schema & Migrations

- [X] T005 [P] Create SQLModel `Task` model based on `data-model.md` in `backend/src/models/task.py`
- [X] T006 Generate initial Alembic migration scripts for `Task` model in `backend/alembic/versions/`
- [X] T007 Apply initial database migrations using `alembic upgrade head`

### MCP Server Setup

- [X] T008 Initialize MCP server using the Official MCP SDK in `backend/src/main.py`
- [X] T009 Integrate FastAPI application for exposing MCP tools (if MCP SDK uses HTTP transport) in `backend/src/main.py`
- [X] T010 Implement MCP tool registration mechanism in `backend/src/api/mcp_tools.py`

### Authentication & Authorization

- [X] T011 Implement JWT validation for tool invocations in `backend/src/core/security.py`
- [X] T012 Implement user ID extraction from JWT for tool invocations in `backend/src/core/security.py`
- [X] T013 Implement task ownership enforcement helper function in `backend/src/services/task_service.py`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: US1 (P1) Add a Todo Task

**Goal**: As a user, I can add new todo tasks, providing details like description and due date via the `add_task` tool.

**Independent Test**: Invoke the `add_task` MCP tool with valid parameters and verify the task is successfully created and retrievable via `list_tasks`.

### Implementation for User Story 1

- [X] T014 [US1] Define `AddTaskInput` and `TaskOutput` Pydantic models in `backend/src/schemas/task.py`
- [X] T015 [US1] Create `TaskService` class skeleton in `backend/src/services/task_service.py`
- [X] T016 [US1] Implement `TaskService.create_task` method to persist new tasks using SQLModel in `backend/src/services/task_service.py`
- [X] T017 [US1] Implement `add_task` tool handler function in `backend/src/tools/todo_tools.py`
- [X] T018 [US1] Register `add_task` tool with MCP server in `backend/src/api/mcp_tools.py`
- [X] T019 [US1] Integrate user authentication and ownership check for `add_task` in `backend/src/tools/todo_tools.py`

**Checkpoint**: User Story 1 should be fully functional and independently testable.

---

## Phase 4: US2 (P1) List Todo Tasks

**Goal**: As a user, I can view a list of my current todo tasks via the `list_tasks` tool.

**Independent Test**: Invoke the `list_tasks` MCP tool and verify that only tasks belonging to the authenticated user are returned, and tasks can be filtered by `is_complete`.

### Implementation for User Story 2

- [X] T020 [US2] Define `ListTasksOutput` Pydantic model in `backend/src/schemas/task.py`
- [X] T021 [US2] Implement `TaskService.get_tasks` method to retrieve tasks using SQLModel, filtered by user ID and `is_complete` in `backend/src/services/task_service.py`
- [X] T022 [US2] Implement `list_tasks` tool handler function in `backend/src/tools/todo_tools.py`
- [X] T023 [US2] Register `list_tasks` tool with MCP server in `backend/src/api/mcp_tools.py`
- [X] T024 [US2] Integrate user authentication and ownership check for `list_tasks` in `backend/src/tools/todo_tools.py`

**Checkpoint**: User Stories 1 AND 2 should both work independently.

---

## Phase 5: US3 (P2) Update a Todo Task

**Goal**: As a user, I can modify the details of an existing todo task via the `update_task` tool.

**Independent Test**: Invoke the `update_task` MCP tool for an owned task and verify the task details are updated. Attempt to update a task not owned by the user and verify failure.

### Implementation for User Story 3

- [X] T025 [US3] Define `UpdateTaskInput` Pydantic model in `backend/src/schemas/task.py`
- [X] T026 [US3] Implement `TaskService.update_task` method to modify task details using SQLModel in `backend/src/services/task_service.py`
- [X] T027 [US3] Ensure task ownership is enforced within `TaskService.update_task` in `backend/src/services/task_service.py`
- [X] T028 [US3] Implement `update_task` tool handler function in `backend/src/tools/todo_tools.py`
- [X] T029 [US3] Register `update_task` tool with MCP server in `backend/src/api/mcp_tools.py`

**Checkpoint**: User Stories 1, 2, and 3 should now be independently functional.

---

## Phase 6: US4 (P2) Complete/Delete a Todo Task

**Goal**: As a user, I can mark a todo task as complete or remove it entirely via the `complete_task` and `delete_task` tools.

**Independent Test**: Invoke `complete_task` and `delete_task` tools for an owned task and verify the task status/existence.

### Implementation for User Story 4

- [X] T030 [US4] Define `CompleteTaskInput`, `DeleteTaskInput`, and `StatusOutput` Pydantic models in `backend/src/schemas/task.py`
- [X] T031 [US4] Implement `TaskService.complete_task` method to update task `is_complete` status in `backend/src/services/task_service.py`
- [X] T032 [US4] Implement `TaskService.delete_task` method to remove tasks using SQLModel in `backend/src/services/task_service.py`
- [X] T033 [US4] Ensure task ownership is enforced in `TaskService.complete_task` and `TaskService.delete_task` in `backend/src/services/task_service.py`
- [X] T034 [US4] Implement `complete_task` tool handler function in `backend/src/tools/todo_tools.py`
- [X] T035 [US4] Implement `delete_task` tool handler function in `backend/src/tools/todo_tools.py`
- [X] T036 [US4] Register `complete_task` tool with MCP server in `backend/src/api/mcp_tools.py`
- [X] T037 [US4] Register `delete_task` tool with MCP server in `backend/src/api/mcp_tools.py`

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and overall system quality.

- [X] T038 [P] Implement robust error handling for tool invocations (e.g., invalid input, non-existent task, authorization failures) in `backend/src/api/errors.py`
- [X] T039 [P] Add logging for all tool invocations and errors in `backend/src/core/logging.py`
- [X] T040 [P] Add unit tests for `Task` SQLModel in `backend/tests/test_models.py`
- [X] T041 [P] Add unit tests for `TaskService` CRUD operations in `backend/tests/test_task_service.py`
- [X] T042 [P] Add unit tests for each tool handler (`add_task`, `list_tasks`, etc.) in `backend/tests/test_todo_tools.py`
- [X] T043 [P] Add integration tests for the MCP server and overall tool invocation flow in `backend/tests/test_mcp_server.py`
- [X] T044 [P] Review and refine MCP tool schemas in `specs/005-mcp-todo-tooling/contracts/openapi.yaml`
- [X] T045 [P] Update `quickstart.md` with detailed instructions for running and testing the MCP server
- [X] T046 [P] Implement performance optimization (e.g., add database indexes for `user_id` on `Task` table) in `backend/alembic/versions/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P2 → P2)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1) Add a Todo Task**: Can start after Foundational (Phase 2)
- **User Story 2 (P1) List Todo Tasks**: Can start after Foundational (Phase 2)
- **User Story 3 (P2) Update a Todo Task**: Can start after Foundational (Phase 2)
- **User Story 4 (P2) Complete/Delete a Todo Task**: Can start after Foundational (Phase 2)

### Within Each User Story

- Models before services
- Services before tool handlers
- Tool handlers before MCP server registration
- Ensure authentication and ownership checks are integrated early.

### Parallel Opportunities

- Many tasks marked [P] can run in parallel (different files, no blocking dependencies).
- Once Foundational phase completes, user stories can be implemented in parallel by different team members.
- Within each story, tasks creating models can run in parallel, followed by service implementations, etc.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1 (Add a Todo Task)
4.  Complete Phase 4: User Story 2 (List Todo Tasks)
5.  **STOP and VALIDATE**: Test User Stories 1 & 2 independently, ensuring basic task creation and retrieval work.
6.  Deploy/demo if ready.

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo (Basic Add Task!)
3.  Add User Story 2 → Test independently → Deploy/Demo (List Tasks!)
4.  Add User Story 3 → Test independently → Deploy/Demo (Update Tasks!)
5.  Add User Story 4 → Test independently → Deploy/Demo (Complete/Delete Tasks!)
6.  Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    -   Developer A: User Story 1 (Add a Todo Task)
    -   Developer B: User Story 2 (List Todo Tasks)
    -   Developer C: User Story 3 (Update a Todo Task)
    -   Developer D: User Story 4 (Complete/Delete a Todo Task)
3.  Stories complete and integrate independently.

---

## Notes

-   Tasks marked [P] indicate parallel execution opportunities.
-   Each user story is designed to be independently completable and testable.
-   Verify components (models, services, tools) work as expected at each checkpoint.
-   Commit after each task or logical group of tasks.
-   Avoid creating tight, cross-story dependencies that break independent testability.
