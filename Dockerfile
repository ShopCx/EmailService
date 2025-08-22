FROM python:3.9-slim

USER root

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements files
COPY requirements*.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Create templates directory if it doesn't exist
RUN mkdir -p templates

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=email_server.py
ENV FLASK_ENV=production
ENV REDIS_URL=redis://localhost:6379
ENV SMTP_SERVER=smtp.gmail.com
ENV SMTP_PORT=587

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start the application
CMD ["python", "email_server.py"]
