# Quickstart: AI Agent & Stateless Chat API

## Overview

This document provides a quick guide to setting up and interacting with the AI Agent and Stateless Chat API feature. This API allows users to communicate with an AI agent using natural language to manage tasks, leveraging MCP tools for actions, with conversation history persisted in a database.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.10+**
*   **Docker** (for running PostgreSQL)
*   **pip** (Python package installer)
*   **git**

## Setup and Installation

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>/backend
    ```

2.  **Set up Python Virtual Environment**:
    ```bash
    python -m venv venv
    ./venv/Scripts/activate # On Windows
    source venv/bin/activate # On Linux/macOS
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Start PostgreSQL Database (using Docker)**:
    Ensure Docker is running.
    ```bash
    # You might need to adjust the Docker command based on your project's docker-compose or direct run command
    docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
    ```
    *Note: Replace `mysecretpassword` with a strong password and ensure the database name and user match your application's configuration (`.env.example`).*

5.  **Run Database Migrations (using Alembic)**:
    ```bash
    alembic upgrade head
    ```

6.  **Configure Environment Variables**:
    Create a `.env` file in the `backend/` directory based on `.env.example` and fill in necessary values, especially for database connection and JWT secret.

## Running the Backend Service

1.  **Start the FastAPI application**:
    ```bash
    uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The API will be available at `http://localhost:8000`.

## Interacting with the API

You can interact with the chat API using `curl` or any API client. Remember to replace `{user_id}` and `YOUR_JWT_TOKEN` with actual values.

**Example: Start a new conversation**

```bash
curl -X POST "http://localhost:8000/api/{user_id}/chat" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-H "Content-Type: application/json" \
-d 
'{
  "last_message": "Hello, what tasks do I have today?"
}'
```

**Example: Continue an existing conversation**

```bash
curl -X POST "http://localhost:8000/api/{user_id}/chat" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-H "Content-Type: application/json" \
-d 
'{
  "last_message": "And what about tomorrow?",
  "conversation_id": "REPLACE_WITH_EXISTING_CONVERSATION_ID"
}'
```

*Note: You will need to implement user registration/login to obtain a `user_id` and `JWT_TOKEN` if not already provided by your system.*
