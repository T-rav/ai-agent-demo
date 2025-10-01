# Production Dockerfile for Python API
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project configuration
COPY pyproject.toml __init__.py ./

# Copy application code (needed for installation)
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir .

# Expose port
EXPOSE 8000

# Run the application with gunicorn
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

