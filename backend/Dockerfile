# Use an official Python image as a base
FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy backend requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the alembic.ini and the backend application code
COPY ../alembic.ini .
COPY src ./src
COPY alembic ./alembic
COPY test_bcrypt.py .
COPY test_server.py .

# Run Alembic migrations
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
RUN alembic upgrade head

# Expose the port FastAPI will run on (from backend/src/config.py)
EXPOSE 7860

# Command to run the FastAPI application
# Use the host and port from config (0.0.0.0:7860) as shown in logs
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]