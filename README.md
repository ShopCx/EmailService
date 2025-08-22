# ShopCx Email Service

An intentionally vulnerable Flask-based email service designed for security testing and educational purposes. This service handles email notifications, template management, and bulk email operations for the ShopCx e-commerce platform.

## Overview

The Email Service is a Python Flask application that provides comprehensive email functionality including template-based emails, bulk sending capabilities, and administrative email management. It integrates with Redis for caching and uses SMTP for email delivery.

## Key Features

- **Template-Based Emails**: Jinja2-powered email templates with dynamic content
- **Bulk Email Operations**: Send emails to multiple recipients efficiently
- **SMTP Integration**: Configurable SMTP server support (Gmail, custom servers)
- **Redis Caching**: Fast template and configuration caching
- **Administrative Tools**: Template management and bulk operations
- **Logging**: Comprehensive email operation logging

## Technology Stack

- **Python 3.9**: Core programming language
- **Flask**: Web framework for REST API
- **Jinja2**: Template engine for email content
- **Redis**: Caching and session storage
- **SMTP**: Email delivery protocol
- **Gunicorn**: WSGI HTTP server
- **Winston**: Structured logging

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/email/send` | Send individual email |
| POST | `/api/email/bulk` | Send bulk emails |
| POST | `/api/email/template` | Create email template |
| POST | `/api/user/settings` | Manage user email settings |
| POST | `/api/user/permissions` | Update user permissions |
| POST | `/api/admin/templates/clear` | Clear all templates (admin) |

## Dependencies

### Required Services
- **Redis Server**: Required for caching and session storage
  - Default URL: `redis://localhost:6379`
- **SMTP Server**: Required for email delivery
  - Default: Gmail SMTP (`smtp.gmail.com:587`)

### Python Dependencies
See `requirements.txt` and `requirements.lock` for full dependency list.

## Build & Run

### Prerequisites
- Python 3.9 or higher
- Redis server running locally
- SMTP server access (Gmail account or custom SMTP)

### Local Development
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export REDIS_URL="redis://localhost:6379"

# Run the service
python email_server.py
```

The service will start on `http://localhost:5000`.

### Docker
```bash
# Build Docker image
docker build -t shopcx-email-service .

# Run container
docker run -p 5000:5000 \
  -e SMTP_USERNAME="your-email@gmail.com" \
  -e SMTP_PASSWORD="your-app-password" \
  shopcx-email-service
```

## Configuration

### Environment Variables
- `SMTP_SERVER`: SMTP server hostname (default: smtp.gmail.com)
- `SMTP_PORT`: SMTP server port (default: 587)
- `SMTP_USERNAME`: SMTP authentication username
- `SMTP_PASSWORD`: SMTP authentication password
- `REDIS_URL`: Redis connection URL
- `FLASK_ENV`: Application environment (development/production)

### Email Templates

Templates are stored in the `templates/` directory:
- `welcome.html`: User welcome email
- `order_confirmation.html`: Order confirmation email
- `notification.html`: Generic notification email

### Template Variables
Templates support Jinja2 syntax with dynamic variables:
```html
<h1>Welcome {{ username }}!</h1>
<p>Your order #{{ order_id }} has been confirmed!</p>
```

## Health Check

The service includes a health check endpoint:
- **Endpoint**: `/health`
- **Returns**: Service status and SMTP/Redis connectivity

## Logging

Email operations are logged to `email.log` with structured JSON format including:
- Timestamp and service name
- Email recipient and subject
- Success/failure status
- Error details for failed operations

## API Usage Examples

### Send Individual Email
```bash
curl -X POST http://localhost:5000/api/email/send \
  -H "Content-Type: application/json" \
  -d '{
    "to": "user@example.com",
    "subject": "Welcome to ShopCx",
    "template": "welcome.html",
    "data": {"username": "John Doe"}
  }'
```

### Send Bulk Email
```bash
curl -X POST http://localhost:5000/api/email/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": ["user1@example.com", "user2@example.com"],
    "subject": "Newsletter",
    "template": "notification.html",
    "data": {"title": "Monthly Update"}
  }'
```

## Security Note

⚠️ **This is an intentionally vulnerable application for security testing purposes. Do not deploy in production environments.**

## Recommended Checkmarx One Configuration
- Criticality: 3
- Cloud Insights: Yes
- Internet-facing: No
