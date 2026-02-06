"""FastAPI application entry point."""
import traceback
from fastapi import Depends, FastAPI, Request, status, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from src import api # Import version info
from src.api.mcp_tools import register_mcp_tools # Import register_mcp_tools at top level

from .config import settings
from .models.database import init_db # Import init_db and get_async_session

from .api.routes.auth import router as auth_router
from .api.working_chat import router as chat_router # Import working chat router
from .api.errors import TaskException, http_exception_handler, task_exception_handler # Import custom error handlers and exceptions
from src.api.routes.tasks import router as tasks_router

from src.services.tool_registry import ToolRegistry # Import ToolRegistry
from src.tools.echo_tool import EchoTool # Import EchoTool

from src.core.logging import configure_structured_logging # Import structured logging config

# Placeholder for MCP SDK import
# In a real scenario, this would be `from mcp_sdk import MCPServer` or similar
class MCPServer:
    def __init__(self):
        self.app = FastAPI(title="MCP Tools", description="MCP Tools API")
        # In a real SDK, tools would be registered here or via a decorator
    
    def as_asgi(self):
        return self.app

# Initialize and mount MCP server globally
mcp_server = MCPServer()  # Define mcp_server before using it

# Configure logging
configure_structured_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting Task API Backend... Router configuration applied.")
    await init_db() # Use await for async init_db
    ToolRegistry.register_tool(EchoTool) # Register EchoTool
    register_mcp_tools(mcp_server) # Pass mcp_server instance
    logger.info("Application startup complete")

    yield

    # Shutdown
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Task API",
    description="RESTful API for task management with user isolation",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Register custom exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(TaskException, task_exception_handler)

# Configure CORS for BetterAuth compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins + ["http://localhost:3000","http://127.0.0.1:3000",],  # Add common frontend ports to existing settings
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    # Expose authorization headers and set-cookie for BetterAuth
    expose_headers=["Access-Control-Allow-Origin", "Set-Cookie", "Authorization"]
)


from src.api.dependencies import verify_user_id, verify_user_from_path # Import verify_user_id and new function

# Include top-level routers in the main app
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

# User-specific router to handle /api/{user_id} and apply authorization
user_specific_router = APIRouter(prefix="/api/{user_id}")

# Include chat router within the user-specific router
user_specific_router.include_router(chat_router, tags=["Chat"], dependencies=[Depends(verify_user_id)])

app.include_router(user_specific_router)  # Include the user-specific router

# Include tasks router at /api/users/{user_id}/tasks to match the frontend expectation
users_tasks_router = APIRouter(prefix="/api/users/{user_id}", dependencies=[Depends(verify_user_from_path)])
users_tasks_router.include_router(tasks_router, tags=["Tasks"])
app.include_router(users_tasks_router)

@user_specific_router.get("/debug-user-id", tags=["Debug"])
async def debug_user_route(user_id: str):
    return {"message": f"User-specific debug route works for user: {user_id}"}



# Dynamically add the user_id path parameter to the prefix of the tasks router


# Mount MCP server after app is created
app.state.mcp_server = mcp_server # Make mcp_server accessible via app.state
app.mount("/mcp", mcp_server.as_asgi())

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Global exception handler - keep as fallback
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    """Handle unexpected exceptions and print full traceback."""
    # Print full traceback to terminal
    traceback.print_exc()

    # Also log error (optional)
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(exc),
                "details": None
            }
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )

