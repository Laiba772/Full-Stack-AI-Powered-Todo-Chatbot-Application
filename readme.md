# AI-Powered Todo Chatbot

An intelligent task management system with natural language processing capabilities. The application allows users to manage their tasks through a conversational AI interface.

## AI Chat Agent

The backend now includes an AI-powered chat agent that allows natural language interaction for task management.

- `POST /api/{user_id}/chat` - Send a message to the AI agent.

For detailed usage instructions, refer to the [AI Chat Agent Quick Start Guide](specs/004-ai-chat-agent/quickstart.md).

## Features

- **Natural Language Processing**: Add, update, and manage tasks using natural language commands
- **AI Assistant**: Conversational interface for task management
- **Task Management**: Create, read, update, and delete tasks
- **User Authentication**: Secure user accounts with JWT-based authentication
- **Real-time Updates**: Instant feedback on task operations
- **Responsive UI**: Modern chat interface for seamless interaction
- **CORS Support**: Properly configured for cross-origin requests

## Tech Stack

- **Backend**: Python, FastAPI, SQLModel, PostgreSQL
- **Frontend**: React, TypeScript
- **AI Integration**: OpenAI API for natural language processing
- **Authentication**: JWT-based authentication system
- **Database**: PostgreSQL with async support

## Project Structure

```
├── backend/              # Backend API server
│   ├── src/
│   │   ├── api/         # API routes and controllers
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic
│   │   └── main.py      # Application entry point
│   ├── requirements.txt # Python dependencies
│   ├── Dockerfile       # Container configuration
│   └── venv/            # Virtual environment (gitignored)
├── frontend/             # Frontend React application
├── specs/                # Project specifications
├── history/              # Project history and records
└── readme.md            # This file
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL
- Docker (optional)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. Run the backend server:
   ```bash
   python -m src.main
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

### Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t ai-todo-chatbot .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 ai-todo-chatbot
   ```

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `GET /api/users/{user_id}/tasks` - Get user's tasks
- `POST /api/users/{user_id}/tasks` - Create a new task
- `PUT /api/users/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/users/{user_id}/tasks/{task_id}` - Delete a task
- `POST /api/{user_id}/chat` - Chat with the AI assistant

## Environment Variables

The application requires the following environment variables:

- `DATABASE_URL` - PostgreSQL database connection string
- `JWT_SECRET` - Secret key for JWT token generation
- `OPENAI_API_KEY` - OpenAI API key for AI functionality
- `BCRYPT_ROUNDS` - Number of bcrypt rounds for password hashing

## Usage

1. Sign up for an account or sign in if you already have one
2. Interact with the AI assistant through the chat interface
3. Use natural language to manage your tasks:
   - "Add a task: Buy groceries"
   - "Show my tasks"
   - "Complete task: Buy groceries"
   - "Delete task: Buy groceries"
4. View your tasks in the task list

## Chat Functionality

The AI assistant understands various commands:
- **Adding tasks**: "Add a task: Complete project", "Create task: Buy milk"
- **Listing tasks**: "Show my tasks", "What are my tasks?", "List tasks"
- **Completing tasks**: "Complete task: Buy groceries", "Mark as done: Finish report"
- **Deleting tasks**: "Delete task: Old task", "Remove task: Cancel appointment"
- **Updating tasks**: "Update task: Change meeting time"

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI for the excellent web framework
- SQLModel for the database ORM
- React for the frontend library
- OpenAI for the AI capabilities
