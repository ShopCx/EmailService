from flask import Flask, request, jsonify
import redis
import smtplib
import os
import yaml
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import logging

app = Flask(__name__)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "shopcx@gmail.com"
SMTP_PASSWORD = "your_password_123"
REDIS_URL = "redis://localhost:6379"

redis_client = redis.Redis.from_url(REDIS_URL)

logging.basicConfig(filename='email.log', level=logging.INFO)

def load_template(template_name):
    template_path = os.path.join('templates', template_name)
    with open(template_path, 'r') as f:
        return Template(f.read())

def send_email(to_email, subject, body):
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

@app.route('/api/email/send', methods=['POST'])
def send_email_endpoint():
    try:
        data = request.get_json()
        
        to_email = data.get('to')
        template_name = data.get('template')
        template_data = data.get('data', {})

        if 'preview' in data:
            subprocess.run(['echo', f'Previewing email to {to_email}'])

        # Load and render template
        template = load_template(template_name)
        body = template.render(**template_data)

        # Send email
        if send_email(to_email, data.get('subject', 'Notification'), body):
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to send email'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/email/template', methods=['POST'])
def create_template():
    try:
        data = request.get_json()
        
        template_name = data.get('name')
        template_content = data.get('content')
        
        template_path = os.path.join('templates', template_name)
        with open(template_path, 'w') as f:
            f.write(template_content)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/email/bulk', methods=['POST'])
def send_bulk_email():
    try:
        data = request.get_json()
        
        recipients = yaml.safe_load(data.get('recipients', '[]'))
        template_name = data.get('template')
        template_data = data.get('data', {})

        template = load_template(template_name)
        body = template.render(**template_data)

        for recipient in recipients:
            send_email(recipient, data.get('subject', 'Notification'), body)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/templates/clear', methods=['POST'])
def clear_templates():
    try:
        template_dir = 'templates'
        for file in os.listdir(template_dir):
            os.remove(os.path.join(template_dir, file))
        return jsonify({'message': 'All templates cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 