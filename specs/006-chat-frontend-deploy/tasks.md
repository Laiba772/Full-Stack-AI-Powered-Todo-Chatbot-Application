# Tasks: ChatKit Frontend & Secure Deployment

**Input**: Design documents from `specs/006-chat-frontend-deploy/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, quickstart.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/src/`

## Phase 1: Setup & Research

**Goal:** Prepare the frontend environment and identify integration points.

**Independent Test**: N/A - Setup phase has no independent test.

**Output**: Updated dependencies, research notes

- [X] T001 Research best practices for integrating OpenAI ChatKit UI components with Next.js/React. (Output: `specs/006-chat-frontend-deploy/research.md`)
- [X] T002 Research secure methods for managing and attaching JWT tokens in Next.js/React applications for backend API calls. (Output: `specs/006-chat-frontend-deploy/research.md`)
- [X] T003 Review existing Todo-Full-Chat frontend structure (`frontend/src/`). (Output: Internal understanding)
- [X] T004 Add ChatKit and required helper libraries to `frontend/package.json`. (Output: Updated `frontend/package.json`)

## Phase 2: Core Chat UI & Backend Communication (US1 - Secure Chat Interaction)

**Goal:** Implement the basic chat UI, connect it to the backend API, and ensure authenticated communication.

**Independent Test**: Send a chat message and verify that the request is authenticated and the response is received successfully, displaying in the UI.

**Output**: Basic functional chat UI, authenticated backend API calls.

- [X] T005 [P] [US1] Build core chat interface components using OpenAI ChatKit (UI only) in `frontend/src/components/chat/`.
- [X] T006 [P] [US1] Create API client for `POST /api/{user_id}/chat` endpoint in `frontend/src/lib/chatApi.ts`.
- [X] T007 [US1] Implement JWT token retrieval and attachment to all backend chat API requests (`frontend/src/hooks/useAuth.ts` or similar).
- [X] T008 [US1] Implement loading states within the chat UI in `frontend/src/components/chat/`.
- [X] T009 [US1] Implement error states within the chat UI in `frontend/src/components/chat/`.
- [X] T010 [US1] Implement confirmation states for successful actions within the chat UI in `frontend/src/components/chat/`.
- [X] T011 [US1] Disable chat input while awaiting backend response in `frontend/src/components/chat/`.

## Phase 3: Conversation Resume & State Management (US2 - Conversation Resume)

**Goal:** Enable seamless conversation resumption across sessions and manage frontend conversation state.

**Independent Test**: Initiate a conversation, close the application, reopen it, and verify that the conversation history is loaded.

**Output**: Chat history visible after reload/login.

- [X] T012 [US2] Implement logic to call `GET /api/{user_id}/chat/history` on page load to fetch conversation history (`frontend/src/hooks/useConversation.ts` or similar).
- [X] T013 [US2] Render messages returned from backend in the chat UI (`frontend/src/components/chat/`).
- [X] T014 [US2] Ensure no conversation IDs are created or stored in the frontend (`frontend/src/lib/chatApi.ts`, `frontend/src/hooks/useConversation.ts`).
- [X] T015 [US2] Implement logic to start a new conversation if no history is found or explicitly requested (`frontend/src/hooks/useConversation.ts`).

## Phase 4: Security & Deployment Configuration

**Goal:** Enforce domain allowlisting and production-safe setup.

**Independent Test**: N/A - Deployment phase tested via E2E/manual validation.

**Output**: Secure frontend configuration.

- [X] T016 Implement a domain allowlisting mechanism in the frontend (e.g., `frontend/src/lib/domainCheck.ts`), preventing chat UI initialization on non-allowlisted domains.
- [X] T017 Add environment variable `NEXT_PUBLIC_CHAT_DOMAIN_KEY` in Next.js project (`.env.local`, `next.config.js`).
- [X] T018 Ensure domain allowlist check runs before chat component mounts (`frontend/src/app/layout.tsx` or similar).
- [X] T019 Verify no OpenAI API keys exist in frontend code (`frontend/src/`).
- [X] T020 Confirm all AI processing occurs only via backend by reviewing code (`frontend/src/`).
- [X] T021 Define production deployment workflow (e.g., Vercel configuration) to enforce domain allowlisting and environment variable usage (`vercel.json`, CI/CD).

## Phase 5: Testing & Validation

**Goal:** Verify functionality, security, and deployment readiness.

**Independent Test**: All previous independent tests and end-to-end scenarios.

**Output**: Fully tested and validated feature.

- [X] T022 [P] Add unit tests for chat components (`frontend/tests/components/chat/`).
- [X] T023 [P] Add unit tests for API client (`frontend/tests/lib/chatApi.test.ts`).
- [X] T024 [P] Add unit tests for state management hooks (`frontend/tests/hooks/`).
- [X] T025 Implement integration tests for authenticated requests (`frontend/tests/integration/chat.test.ts`).
- [X] T026 Implement E2E tests for sending messages and conversation resume (`frontend/e2e/chat.spec.ts`).
- [X] T027 Implement security tests to verify no sensitive data leakage and proper authentication/authorization enforcement (`frontend/tests/security/`).
- [X] T028 Test on allowlisted domain → should work (Manual/E2E test).
- [X] T029 Test on non-allowlisted domain → should fail (Manual/E2E test).
- [X] T030 Inspect browser network tab to confirm only backend API calls (Manual test).
- [X] T031 Validate the `quickstart.md` by following its steps end-to-end for frontend setup and deployment.

---
## Dependencies & Execution Order
- Phase 1: Setup & Research (must complete before other phases)
- Phase 2: Core Chat UI & Backend Communication (depends on Phase 1)
- Phase 3: Conversation Resume & State Management (depends on Phase 2)
- Phase 4: Security & Deployment Configuration (can be parallel to Phase 2/3 but needs core UI to exist)
- Phase 5: Testing & Validation (depends on all previous phases)

## Implementation Strategy
- **MVP First**: Focus on completing Phase 1 and Phase 2 for a basic, authenticated chat.
- **Incremental Delivery**: Gradually add conversation resume (Phase 3) and then security/deployment (Phase 4), testing at each stage.
