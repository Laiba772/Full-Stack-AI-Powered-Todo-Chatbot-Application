# Quickstart: MCP Server & Todo Tooling

## Overview

This document provides a quick guide to setting up and running the MCP (Model Context Protocol) server that exposes Todo operations as tools. These tools allow external AI agents to manage user tasks, ensuring stateless operation, database persistence, and JWT-authenticated user ownership enforcement.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.10+**
*   **pip** (Python package installer)
*   **git**
*   **Official MCP SDK for Python** (will be installed as part of dependencies)

## Setup and Installation

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>/backend
    ```

2.  **Set up Python Virtual Environment**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate # On Windows
    source venv/bin/activate # On Linux/macOS
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create Database Tables (using SQLModel)**:
    This project uses SQLite for development by default. You can create the necessary tables by running a temporary script.
    ```bash
    # Ensure you are in the 'backend' directory
    python -c "from src.models.database import engine; from sqlmodel import SQLModel; SQLModel.metadata.create_all(engine)"
    ```
    *Note: For production, you would typically use PostgreSQL and Alembic for migrations. Refer to the `alembic` directory and `backend/.env.example` for PostgreSQL configuration.*

5.  **Configure Environment Variables**:
    Create a `.env` file in the `backend/` directory based on `.env.example` and fill in necessary values, especially for database connection and JWT secret.

## Running the MCP Server

The MCP server is integrated into the main FastAPI application (`backend/src/main.py`). Once the FastAPI application is running, the MCP tools will be exposed under the `/mcp/` path.

1.  **Start the Backend application (which hosts the MCP server)**:
    ```bash
    # Ensure you are in the 'backend' directory
    uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The MCP server, exposing the tools, will be available at `http://localhost:8000/mcp/`.

## Invoking MCP Tools (Conceptual)

MCP tools are designed to be invoked by an AI agent using the MCP SDK. Below is a conceptual example of how an AI agent (or a developer testing the tools) would interact with the tools via HTTP requests, assuming an MCP client library handles authentication and request formatting.

First, you would need to obtain a JWT token for an authenticated user (e.g., via the `/api/auth/token` endpoint).

```python
# Pseudo-code example for illustration using requests library

import requests
from datetime import datetime
from uuid import UUID

BASE_URL = "http://localhost:8000/mcp"
AUTH_TOKEN = "YOUR_JWT_TOKEN_HERE" # Replace with a valid JWT token for an existing user

headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}

# Example: Add a new task
try:
    add_payload = {
        "description": "Prepare presentation for team meeting",
        "due_date": datetime.utcnow().isoformat()
    }
    response = requests.post(f"{BASE_URL}/add_task", headers=headers, json=add_payload)
    response.raise_for_status()
    new_task = response.json()
    print("Task added successfully:", new_task)
    new_task_id = new_task["task_id"]
except requests.exceptions.RequestException as e:
    print("Error adding task:", e)
    new_task_id = None

# Example: List tasks
try:
    response = requests.get(f"{BASE_URL}/list_tasks", headers=headers)
    response.raise_for_status()
    tasks_list = response.json()
    print("Your tasks:", tasks_list)
except requests.exceptions.RequestException as e:
    print("Error listing tasks:", e)


# Example: Update a task (assuming new_task_id was obtained from add_task)
if new_task_id:
    try:
        update_payload = {
            "task_id": str(new_task_id),
            "description": "Finalize presentation slides",
            "is_complete": True
        }
        response = requests.post(f"{BASE_URL}/update_task", headers=headers, json=update_payload)
        response.raise_for_status()
        updated_task = response.json()
        print("Task updated successfully:", updated_task)
    except requests.exceptions.RequestException as e:
        print("Error updating task:", e)


# Example: Complete a task (assuming new_task_id)
if new_task_id:
    try:
        complete_payload = {"task_id": str(new_task_id)}
        response = requests.post(f"{BASE_URL}/complete_task", headers=headers, json=complete_payload)
        response.raise_for_status()
        status_output = response.json()
        print("Task completed successfully:", status_output)
    except requests.exceptions.RequestException as e:
        print("Error completing task:", e)

# Example: Delete a task (assuming new_task_id)
if new_task_id:
    try:
        delete_payload = {"task_id": str(new_task_id)}
        response = requests.post(f"{BASE_URL}/delete_task", headers=headers, json=delete_payload)
        response.raise_for_status()
        status_output = response.json()
        print("Task deleted successfully:", status_output)
    except requests.exceptions.RequestException as e:
        print("Error deleting task:", e)

```
*Note: The actual client-side implementation would depend on the specific MCP SDK usage and how it integrates with your AI agent framework.*
