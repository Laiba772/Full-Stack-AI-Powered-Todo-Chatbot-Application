# Data Model for MCP Server & Todo Tooling

## Entities

### User

Represents an authenticated individual who owns todo tasks. This entity is shared with the AI Agent & Stateless Chat API feature.

-   **Fields**:
    -   `id`: UUID (Primary Key, unique identifier for the user)
    -   `username`: String (Unique, required, e.g., 'john_doe')
    -   `email`: String (Unique, required, e.g., 'john.doe@example.com')
    -   `password_hash`: String (Required, securely stored hashed password)
    -   `created_at`: Datetime (Timestamp of user creation)
    -   `updated_at`: Datetime (Timestamp of last update)
-   **Relationships**:
    -   One-to-many with Task (a User can have multiple Tasks)
-   **Validation Rules**:
    -   `username` and `email` must be unique across all users.
    -   `email` must conform to a valid email address format.

### Task

Represents a single todo item belonging to a user.

-   **Fields**:
    -   `id`: UUID (Primary Key, unique identifier for the task)
    -   `user_id`: UUID (Foreign Key, links to User.id, required)
    -   `description`: String (Required, the main content of the todo task, e.g., "Buy groceries")
    -   `due_date`: Datetime (Optional, a timestamp for when the task is due)
    -   `is_complete`: Boolean (Required, default `False`, indicates if the task is completed)
    -   `created_at`: Datetime (Timestamp of task creation)
    -   `updated_at`: Datetime (Timestamp of last update)
-   **Relationships**:
    -   Many-to-one with User (each Task belongs to one User)
-   **Validation Rules**:
    -   `user_id` must reference an existing User record.
    -   `description` cannot be empty and should have a reasonable length limit (e.g., 255 characters).
    -   `is_complete` defaults to `False` upon creation.
