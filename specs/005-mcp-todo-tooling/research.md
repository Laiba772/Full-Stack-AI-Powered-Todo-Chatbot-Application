# Research for MCP Server & Todo Tooling

## Official MCP SDK and Server Setup

-   **Decision**: The Official MCP SDK for Python will be used to initialize the MCP server.
-   **Rationale**: The `spec.md` explicitly requires using the "Official MCP SDK". The web search confirmed its availability and suitability for building MCP servers and clients.
-   **Key Considerations**:
    *   Determine the appropriate version of the Python SDK (v1.x or v2 development). For initial implementation, v1.x will be targeted for stability, with a plan to upgrade to v2 when stable.
    *   Understand server setup mechanisms (e.g., transport protocols like stdio, SSE, Streamable HTTP). Streamable HTTP is likely most suitable for a web-based backend.

## MCP Tool Interfaces and Schemas

-   **Decision**: Tool interfaces and schemas will be defined using Python type hints and Pydantic models (leveraging SQLModel's capabilities).
-   **Rationale**: The `spec.md` requires defining "Tool schemas, parameters, and return formats". The MCP SDK likely integrates well with standard Python typing and validation libraries. Pydantic (used by SQLModel) is a natural fit for this.
-   **Implementation**: Each required tool (`add_task`, `list_tasks`, `update_task`, `complete_task`, `delete_task`) will have a corresponding input schema (Pydantic model) and a defined return format.

## Tool Handlers and SQLModel Integration

-   **Decision**: Tool handlers will be implemented as Python functions that accept validated input schemas and interact with the PostgreSQL database using SQLModel.
-   **Rationale**: The `spec.md` requires "Database-backed task operations via SQLModel". SQLModel provides a convenient way to define models and interact with the database, ensuring type safety and reducing boilerplate.
-   **Implementation**: Each tool handler will perform CRUD operations on the `Task` entity (and potentially `User` for ownership checks) using SQLModel sessions.

## JWT-based User Validation

-   **Decision**: User identity enforcement will be handled by extracting the `user_id` from a JWT provided in the request headers (as per the existing authentication scheme).
-   **Rationale**: The `spec.md` requires "JWT-authenticated user identity enforcement" and "User ID must be validated for every tool call". This aligns with the project's existing authentication mechanism.
-   **Implementation**: A dependency injection mechanism (e.g., FastAPI `Depends`) will be used to get the authenticated user and validate `user_id` for every tool invocation.

## Stateless Tools and Database-Driven Operations

-   **Decision**: All tool implementations will strictly adhere to stateless principles, with all necessary data being passed in the tool invocation and all state changes persisted immediately to the database.
-   **Rationale**: The `spec.md` explicitly states "Tools must be stateless" and "Tools must not rely on in-memory state". The `constitution.md` also emphasizes a "Fully Stateless Server Architecture" and "Database-Backed Conversation Memory".
-   **Implementation**: Tool handlers will not store any internal state between invocations. Database transactions will be used to ensure atomicity and consistency of state changes.

## Tool Behavior Validation

-   **Decision**: Tool behavior will be validated through a combination of unit tests for individual tool handlers and integration tests for the overall MCP server setup.
-   **Rationale**: The `spec.md` requires "Validate tool behavior with example inputs/outputs" and "Tool behavior is deterministic and reproducible".
-   **Implementation**: Unit tests will cover input validation, database interactions, and expected outputs for each tool. Integration tests will simulate tool invocations through the MCP server and verify end-to-end functionality.
