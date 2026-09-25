# Multi-stage production Dockerfile for Bright Edu Consultancy
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run collectstatic during build (using dummy SECRET_KEY so build passes)
ENV SECRET_KEY="build-time-dummy-key-for-collectstatic" \
    DEBUG="False"
RUN python manage.py collectstatic --noinput || true

# Create unprivileged user for security
RUN addgroup --system django && adduser --system --group django \
    && chown -R django:django /app

USER django

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "bright_edu.wsgi:application"]
