# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY backend/requirements-prod.txt /app/
RUN pip install --upgrade pip && pip install -r requirements-prod.txt

# Copy backend code
COPY backend/ /app/

# Expose the port (fly.io will set $PORT)
EXPOSE 8080

# Set environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Start the app with Gunicorn for production
CMD ["gunicorn", "--factory", "-b", "0.0.0.0:8080", "-w", "1", "-t", "1", "app:create_app"]
