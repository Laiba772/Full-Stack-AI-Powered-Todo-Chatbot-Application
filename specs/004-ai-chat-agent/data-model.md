# Data Model for AI Agent & Stateless Chat API

## Entities

### User

Represents an authenticated individual interacting with the chat.

-   **Fields**:
    -   `id`: UUID (Primary Key, unique identifier for the user)
    -   `username`: String (Unique, required, e.g., 'john_doe')
    -   `email`: String (Unique, required, e.g., 'john.doe@example.com')
    -   `password_hash`: String (Required, securely stored hashed password)
    -   `created_at`: Datetime (Timestamp of user creation)
    -   `updated_at`: Datetime (Timestamp of last update)
-   **Relationships**:
    -   One-to-many with Conversation (a User can have multiple Conversations)
-   **Validation Rules**:
    -   `username` and `email` must be unique across all users.
    -   `email` must conform to a valid email address format.

### Conversation

Represents a sequence of messages exchanged between a user and the AI agent within a single chat session.

-   **Fields**:
    -   `id`: UUID (Primary Key, unique identifier for the conversation)
    -   `user_id`: UUID (Foreign Key, links to User.id, required)
    -   `title`: String (Optional, user-provided or auto-generated title for the conversation, e.g., "Planning Project Alpha")
    -   `created_at`: Datetime (Timestamp of conversation initiation)
    -   `updated_at`: Datetime (Timestamp of last message in the conversation)
-   **Relationships**:
    -   Many-to-one with User (each Conversation belongs to one User)
    -   One-to-many with Message (each Conversation can have multiple Messages)
-   **Validation Rules**:
    -   `user_id` must reference an existing User record.

### Message

Represents a single turn or utterance within a conversation, either from the user or the AI agent.

-   **Fields**:
    -   `id`: UUID (Primary Key, unique identifier for the message)
    -   `conversation_id`: UUID (Foreign Key, links to Conversation.id, required)
    -   `sender`: Enum (Required, identifies who sent the message: 'user' or 'ai_agent')
    -   `content`: Text (Required, the actual text content of the message)
    -   `timestamp`: Datetime (Required, recorded time when the message was sent/received)
    -   `tool_calls`: JSON (Optional, stores details if the AI agent invoked tools, e.g., tool name, arguments)
    -   `tool_output`: JSON (Optional, stores the output returned by tool invocations)
-   **Relationships**:
    -   Many-to-one with Conversation (each Message belongs to one Conversation)
-   **Validation Rules**:
    -   `conversation_id` must reference an existing Conversation record.
    -   `sender` must be one of the predefined values ('user', 'ai_agent').
    -   `content` cannot be empty.
