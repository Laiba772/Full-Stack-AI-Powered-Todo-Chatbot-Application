# Tasks: AI Agent & Stateless Chat API

**Input**: Design documents from `/specs/004-ai-chat-agent/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below assume `backend/src/` as the primary development focus for this feature.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [X] T001 Initialize Python environment and install dependencies from `backend/requirements.txt`
- [X] T002 Configure environment variables from `backend/.env.example` to `backend/.env`
- [X] T003 Review and update `backend/Dockerfile` for deployment readiness
- [X] T004 Review and update `backend/alembic.ini` for database migrations configuration

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

### Database Schema & Migrations

- [X] T005 [P] Create SQLAlchemy User model based on `data-model.md` in `backend/src/models/user.py`
- [X] T006 [P] Create SQLAlchemy Conversation model based on `data-model.md` in `backend/src/models/conversation.py`
- [X] T007 [P] Create SQLAlchemy Message model based on `data-model.md` in `backend/src/models/message.py`
- [X] T008 Generate initial Alembic migration scripts for User, Conversation, Message models in `backend/alembic/versions/`
- [X] T009 Apply initial database migrations using `alembic upgrade head`

### Authentication & Authorization

- [X] T010 Implement JWT token generation utility in `backend/src/core/security.py`
- [X] T011 Implement JWT token validation utility in `backend/src/core/security.py`
- [X] T012 Create `get_current_user` dependency for authenticated user extraction from JWT in `backend/src/api/dependencies.py`
- [X] T013 Implement user ID matching (path `user_id` vs. authenticated user ID) for API access control in `backend/src/api/dependencies.py`

### Core API Structure

- [X] T014 Initialize FastAPI application instance in `backend/src/main.py`
- [X] T015 Integrate CORS middleware configuration in `backend/src/main.py`
- [X] T016 Register API routers for chat functionality in `backend/src/main.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: US1 (P1) Natural Language Interaction

**Goal**: As a user, I can send a natural language message to the AI agent and receive an appropriate response.

**Independent Test**: Send a natural language query to `POST /api/{user_id}/chat` with no `conversation_id` and verify a relevant AI response (without tool invocation).

### Implementation for User Story 1

- [X] T017 [US1] Create `AIAgentService` class skeleton in `backend/src/services/ai_agent_service.py`
- [X] T018 [US1] Implement initial OpenAI Agents SDK configuration in `backend/src/config.py`
- [X] T019 [US1] Define initial agent system prompt and behavior rules in `backend/src/config.py`
- [X] T020 [US1] Implement `ChatService` skeleton with message persistence methods in `backend/src/services/chat_service.py`
- [X] T021 [US1] Implement `POST /api/{user_id}/chat` endpoint skeleton in `backend/src/api/chat_api.py`
- [X] T022 [US1] Integrate `get_current_user` and `user_id` matching in `POST /api/{user_id}/chat` in `backend/src/api/chat_api.py`
- [X] T023 [US1] Implement basic natural language processing to generate initial AI response (no tool invocation) in `backend/src/services/ai_agent_service.py`
- [X] T024 [US1] Persist user's message to database via `ChatService` in `backend/src/services/chat_service.py`
- [X] T025 [US1] Persist AI agent's response to database via `ChatService` in `backend/src/services/chat_service.py`
- [X] T026 [US1] Return AI agent's response from `POST /api/{user_id}/chat` including `conversation_id` and `message`

**Checkpoint**: User Story 1 should be fully functional and independently testable.

---

## Phase 4: US2 (P1) Multi-Turn Conversation

**Goal**: As a user, I can continue an existing conversation with the AI agent, and it maintains context from previous messages.

**Independent Test**: Initiate a conversation, send subsequent messages using the returned `conversation_id`, and verify the AI agent's responses are contextually aware of the full conversation history.

### Implementation for User Story 2

- [X] T027 [US2] Implement conversation retrieval from database using `conversation_id` in `backend/src/services/chat_service.py`
- [X] T028 [US2] Implement conversation history reconstruction for AI agent context in `backend/src/services/ai_agent_service.py`
- [X] T029 [US2] Modify `POST /api/{user_id}/chat` to accept optional `conversation_id` in `backend/src/api/chat_api.py`
- [X] T030 [US2] Update `ChatService` to use existing conversation or create new one based on `conversation_id` in `backend/src/services/chat_service.py`
- [X] T031 [US2] Ensure AI agent maintains context across multiple turns using reconstructed history in `backend/src/services/ai_agent_service.py`
- [X] T032 [US2] Update Conversation `updated_at` timestamp on new messages in `backend/src/services/chat_service.py`

**Checkpoint**: User Stories 1 AND 2 should both work independently.

---

## Phase 5: US3 (P2) AI Agent Tool Chaining

**Goal**: As a user, I can make requests that trigger the AI agent to invoke and chain multiple MCP tools for complex tasks.

**Independent Test**: Make a natural language request (e.g., "Summarize my tasks for today and then add a reminder for tomorrow") that requires the AI agent to invoke multiple simulated tools, verifying the chained actions and final response.

### Implementation for User Story 3

- [X] T033 [US3] Implement `ToolRegistry` for MCP tool registration in `backend/src/services/tool_registry.py`
- [X] T034 [US3] Implement MCP tool invocation mechanism within `AIAgentService` in `backend/src/services/ai_agent_service.py`
- [X] T035 [US3] Develop a mock MCP tool (e.g., `TaskSummaryTool` and `ReminderTool`) in `backend/src/tools/`
- [X] T036 [US3] Register mock MCP tools with `ToolRegistry` on application startup in `backend/src/main.py`
- [X] T037 [US3] Integrate registered MCP tools into AI agent's capabilities (OpenAI Agents SDK configuration) in `backend/src/services/ai_agent_service.py`
- [X] T038 [US3] Implement deterministic mapping of natural language to tool calls in `backend/src/services/ai_agent_service.py`
- [X] T039 [US3] Enable chaining of multiple tool calls within a single AI agent turn in `backend/src/services/ai_agent_service.py`
- [X] T040 [US3] Store `tool_calls` and `tool_output` in `Message` model when tools are used in `backend/src/services/chat_service.py`
- [X] T041 [US3] Update `POST /api/{user_id}/chat` response to indicate `tool_invoked` status based on `AIAgentService` output

**Checkpoint**: User Stories 1, 2, and 3 should now be independently functional.

---

## Phase 6: US4 (P2) Robust Error Handling

**Goal**: As a user, I receive clear and helpful explanations from the AI agent and API when errors occur.

**Independent Test**: Trigger various error conditions (e.g., invalid `conversation_id`, tool invocation failure, invalid JWT) and verify the API returns appropriate error responses and the AI agent provides user-friendly explanations.

### Implementation for User Story 4

- [X] T042 [US4] Implement centralized exception handling for API errors in `backend/src/api/`
- [X] T043 [US4] Implement specific error handling for failed tool invocations in `backend/src/services/ai_agent_service.py`
- [X] T044 [US4] Implement handling for ambiguous natural language requests leading to unclear agent actions
- [X] T045 [US4] Implement database connection error handling for `ChatService` persistence/retrieval operations
- [X] T046 [US4] Ensure `AIAgentService` provides clear, friendly explanations for internal errors to the user
- [X] T047 [US4] Return API error responses (400, 401, 403, 500) as per `openapi.yaml` spec from `backend/src/api/chat_api.py`

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and overall system quality.

- [X] T048 [P] Implement structured logging for API requests and AI agent interactions in `backend/src/core/logging.py`
- [X] T049 [P] Review and refine API documentation in `specs/004-ai-chat-agent/contracts/openapi.yaml`
- [X] T050 [P] Add unit tests for `AIAgentService` in `backend/tests/test_ai_agent_service.py`
- [X] T051 [P] Add unit tests for `ChatService` in `backend/tests/test_chat_service.py`
- [X] T052 [P] Add integration tests for `POST /api/{user_id}/chat` endpoint in `backend/tests/test_chat_api.py`
- [X] T053 [P] Add tests for database models and CRUD operations in `backend/tests/test_models.py`
- [X] T054 [P] Review and apply security best practices (e.g., input sanitization) in `backend/src/api/chat_api.py`
- [X] T055 [P] Consider performance optimization techniques (e.g., database indexing for conversation history)
- [X] T056 [P] Validate `quickstart.md` by following its steps end-to-end

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

- **User Story 1 (P1) Natural Language Interaction**: Can start after Foundational (Phase 2)
- **User Story 2 (P1) Multi-Turn Conversation**: Can start after Foundational (Phase 2)
- **User Story 3 (P2) AI Agent Tool Chaining**: Can start after Foundational (Phase 2)
- **User Story 4 (P2) Robust Error Handling**: Can start after Foundational (Phase 2)

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration

### Parallel Opportunities

- Many tasks marked [P] can run in parallel (different files, no blocking dependencies).
- Once Foundational phase completes, user stories can be implemented in parallel by different team members.
- Within each story, tasks creating models can run in parallel, followed by service implementations, etc.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1 (Natural Language Interaction)
4.  Complete Phase 4: User Story 2 (Multi-Turn Conversation)
5.  **STOP and VALIDATE**: Test User Stories 1 & 2 independently, ensuring core chat functionality and persistence work.
6.  Deploy/demo if ready.

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo (Basic Chat MVP!)
3.  Add User Story 2 → Test independently → Deploy/Demo (Contextual Chat!)
4.  Add User Story 3 → Test independently → Deploy/Demo (Tool-Powered Chat!)
5.  Add User Story 4 → Test independently → Deploy/Demo (Robust Chat!)
6.  Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    -   Developer A: User Story 1 (Natural Language Interaction)
    -   Developer B: User Story 2 (Multi-Turn Conversation)
    -   Developer C: User Story 3 (AI Agent Tool Chaining)
    -   Developer D: User Story 4 (Robust Error Handling)
3.  Stories complete and integrate independently.

---

## Notes

-   Tasks marked [P] indicate parallel execution opportunities.
-   Each user story is designed to be independently completable and testable.
-   Verify components (models, services, APIs) work as expected at each checkpoint.
-   Commit after each task or logical group of tasks.
-   Avoid creating tight, cross-story dependencies that break independent testability.
