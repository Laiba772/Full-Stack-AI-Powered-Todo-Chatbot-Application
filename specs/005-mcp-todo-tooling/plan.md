# Implementation Plan: MCP Server & Todo Tooling

**Branch**: `005-mcp-todo-tooling` | **Date**: 2026-01-24 | **Spec**: specs/005-mcp-todo-tooling/spec.md
**Input**: Feature specification from `/specs/005-mcp-todo-tooling/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan details the implementation of an MCP (Model Context Protocol) server responsible for exposing Todo operations (add, list, update, complete, delete tasks) as stateless tools. The server will be set up using the Official MCP SDK for Python, with task data managed via SQLModel and persisted in a PostgreSQL database. All tool invocations will enforce JWT-authenticated user identity and ensure strict task ownership, preventing cross-user data access.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: Official MCP SDK (Python), SQLModel, FastAPI (implied by MCP SDK/server setup), PostgreSQL client library
**Storage**: PostgreSQL
**Testing**: Pytest
**Target Platform**: Linux server (containerized deployment)
**Project Type**: Backend service/MCP server
**Performance Goals**:
- Response time for `add_task`, `update_task`, `complete_task`, `delete_task` is under 200ms for 99% of requests.
- Response time for `list_tasks` is under 500ms for 99% of requests, even with 1000 tasks per user.
**Constraints**:
- MCP tools must be stateless and not rely on in-memory state.
- User ID must be validated for every tool call.
- All operations must enforce task ownership.
- Tools must operate deterministically.
**Scale/Scope**: Supports 10,000 concurrent users performing task operations.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Natural Language Interface**: This feature provides the tooling for the AI; the NL interface is handled by the AI Agent feature. It supports the NL interface by providing robust tools.
- [x] **Tool-Driven AI**: This feature directly implements the MCP tools that the AI agent will invoke.
- [x] **Stateless Architecture**: The plan explicitly states that MCP tools must be stateless and not rely on in-memory state.
- [x] **Database-Backed Memory**: Task operations are explicitly backed by a PostgreSQL database via SQLModel.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/           # SQLModel definitions for Task, and potentially User if needed for relationships
│   ├── services/         # Business logic for Todo operations, integrating with SQLModel
│   ├── api/              # Entrypoint for the MCP server, registering tools
│   └── tools/            # Definitions and handlers for MCP tools (add_task, list_tasks, etc.)
└── tests/                # Unit and integration tests for tools, services, and models
```

**Structure Decision**: The "Backend service" structure is selected, extending the existing `backend/` directory with specific modules for MCP tools and SQLModel entities.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
