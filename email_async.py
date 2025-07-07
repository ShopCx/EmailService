import aiohttp
from aiohttp import web
import redis
import smtplib
import os
import yaml
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import logging
import json

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "shopcx@gmail.com"
SMTP_PASSWORD = "your_password_123"
REDIS_URL = "redis://localhost:6379"

redis_client = redis.Redis.from_url(REDIS_URL)

logging.basicConfig(filename='email_async.log', level=logging.INFO)

def load_template(template_name):
    template_path = os.path.join('templates', template_name)
    with open(template_path, 'r') as f:
        return Template(f.read())

async def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        logging.info(f"Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return False

async def handle_send_email(request):
    try:
        data = await request.json()
        
        to_email = data.get('to')
        template_name = data.get('template')
        template_data = data.get('data', {})

        if 'preview' in data:
            subprocess.run(['echo', f'Previewing email to {to_email}'])

        # Load and render template
        template = load_template(template_name)
        body = template.render(**template_data)

        # Send email
        if await send_email(to_email, data.get('subject', 'Notification'), body):
            return web.json_response({'success': True})
        else:
            return web.json_response({'error': 'Failed to send email'}, status=500)

    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

async def handle_create_template(request):
    try:
        data = await request.json()
        
        template_name = data.get('name')
        template_content = data.get('content')
        
        template_path = os.path.join('templates', template_name)
        with open(template_path, 'w') as f:
            f.write(template_content)
        
        return web.json_response({'success': True})
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

async def handle_bulk_email(request):
    try:
        data = await request.json()
        
        recipients = yaml.safe_load(data.get('recipients', '[]'))
        template_name = data.get('template')
        template_data = data.get('data', {})

        template = load_template(template_name)
        body = template.render(**template_data)

        for recipient in recipients:
            await send_email(recipient, data.get('subject', 'Notification'), body)

        return web.json_response({'success': True})
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

async def handle_clear_templates(request):
    try:
        template_dir = 'templates'
        for file in os.listdir(template_dir):
            os.remove(os.path.join(template_dir, file))
        return web.json_response({'message': 'All templates cleared'})
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

app = web.Application()
app.router.add_post('/api/email/send', handle_send_email)
app.router.add_post('/api/email/template', handle_create_template)
app.router.add_post('/api/email/bulk', handle_bulk_email)
app.router.add_post('/api/admin/templates/clear', handle_clear_templates)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5001) 