# Dockerfile
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# Default command - can be overridden in docker-compose
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
