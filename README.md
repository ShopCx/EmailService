# ShopCx Email Service

A Flask-based email service for the ShopCx demo application with intentionally vulnerable endpoints. This service handles email notifications, template management, and bulk email operations for the e-commerce platform.

## Security Note

⚠️ **This is an intentionally vulnerable application for security testing purposes. Do not deploy in production or sensitive environments.**

## Overview

The Email Service is a Python Flask application that provides comprehensive email functionality including template-based emails, bulk sending capabilities, and administrative email management. It integrates with Redis for caching and uses SMTP for email delivery with intentionally vulnerable command injection patterns.

## Key Features

- **Template-Based Emails**: Jinja2-powered email templates with dynamic content
- **Bulk Email Operations**: Send emails to multiple recipients efficiently
- **SMTP Integration**: Configurable SMTP server support (Gmail, custom servers)
- **Redis Caching**: Fast template and configuration caching
- **Administrative Tools**: Template management and bulk operations
- **Logging**: Comprehensive email operation logging
- **Command Execution**: Preview functionality with subprocess execution
- **YAML Processing**: Dynamic recipient list processing
- **Template Management**: Create and clear email templates
- **File System Operations**: Template file handling

## Technology Stack

- **Python 3.9**: Core programming language
- **Flask**: Web framework for REST API
- **Jinja2**: Template engine for email content
- **Redis**: Caching and session storage
- **SMTP**: Email delivery protocol
- **PyYAML**: YAML processing for bulk operations
- **Subprocess**: Command execution for preview functionality
- **Cryptography**: Security utilities (included)
- **Gunicorn**: WSGI HTTP server (included)
- **Django**: Web framework (included but unused)
- **Requests**: HTTP client library (included)
- **BeautifulSoup4**: HTML parsing (included)
- **Aiohttp**: Async HTTP client (included)
