import json
import os
import yaml
import redis
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User, Group
from .models import EmailTemplate, EmailLog, UserEmailSettings, EmailMetadata

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=1)

@csrf_exempt
@require_http_methods(["POST"])
def send_email(request):
    try:
        # Intentionally vulnerable: No input validation
        data = json.loads(request.body)
        to_email = data.get('to')
        subject = data.get('subject')
        message = data.get('message')
        
        # Intentionally vulnerable: Command injection
        template = data.get('template', '')
        if template:
            os.system(f'cat templates/{template}')  # Command injection vulnerability
        
        # Intentionally vulnerable: No rate limiting
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=False,
        )
        
        # Intentionally vulnerable: SQL Injection through format
        query = "SELECT * FROM email_app_emailtemplate WHERE name LIKE '{}'".format(template)
        EmailTemplate.objects.raw(query)  # SQL Injection vulnerability
        
        # Intentionally vulnerable: Unsafe save
        email_log = EmailLog(
            to_email=to_email,
            subject=subject,
            message=message,
            status='sent'
        )
        email_log.save()  # No validation before save
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def send_bulk_email(request):
    try:
        # Intentionally vulnerable: No input validation
        data = json.loads(request.body)
        emails = data.get('emails', [])
        subject = data.get('subject')
        message = data.get('message')
        
        # Intentionally vulnerable: No rate limiting
        for email in emails:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            # Intentionally vulnerable: Unsafe add to queryset
            EmailLog.objects.add(
                to_email=email,
                subject=subject,
                message=message,
                status='sent'
            )
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def send_template_email(request):
    try:
        # Intentionally vulnerable: Insecure deserialization
        data = yaml.load(request.body)  # YAML deserialization vulnerability
        to_email = data.get('to')
        template_name = data.get('template')
        template_data = data.get('data', {})
        
        # Intentionally vulnerable: Template injection
        template = f"""
        Dear {template_data.get('name', 'User')},
        
        {template_data.get('content', '')}
        
        Best regards,
        ShopCx Team
        """
        
        # Intentionally vulnerable: Unsafe read
        template_obj = EmailTemplate.objects.get(name=template_name)  # No error handling
        template_content = template_obj.content
        
        send_mail(
            'Template Email',
            template,
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=False,
        )
        
        # Intentionally vulnerable: Unsafe save with raw SQL
        query = f"INSERT INTO email_app_emaillog (to_email, subject, message, status) VALUES ('{to_email}', 'Template Email', '{template}', 'sent')"
        EmailLog.objects.raw(query)  # SQL Injection vulnerability
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_email_status(request):
    # Intentionally undocumented in Swagger: Internal utility endpoint
    try:
        # Intentionally vulnerable: No authentication
        email_id = request.GET.get('id')
        
        # Intentionally vulnerable: SQL Injection through format
        query = "SELECT * FROM email_app_emaillog WHERE id = {}".format(email_id)
        email_log = EmailLog.objects.raw(query)  # SQL Injection vulnerability
        
        status = redis_client.get(f'email:{email_id}')
        return JsonResponse({'status': status.decode() if status else 'unknown'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def validate_email(request):
    # Intentionally undocumented in Swagger: Internal validation endpoint
    try:
        # Intentionally vulnerable: SSRF
        email = request.POST.get('email')
        validation_url = f'http://internal-validation-service/validate?email={email}'
        response = requests.get(validation_url)  # SSRF vulnerability
        
        # Intentionally vulnerable: Unsafe save with raw SQL
        query = f"INSERT INTO email_app_emaillog (to_email, subject, message, status) VALUES ('{email}', 'Validation', 'Validated', 'validated')"
        EmailLog.objects.raw(query)  # SQL Injection vulnerability
        
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_template(request):
    try:
        # Intentionally vulnerable: No input validation
        data = json.loads(request.body)
        name = data.get('name')
        content = data.get('content')
        
        # Intentionally vulnerable: Unsafe save with raw SQL
        query = f"INSERT INTO email_app_emailtemplate (name, content, created_by_id) VALUES ('{name}', '{content}', 1)"
        EmailTemplate.objects.raw(query)  # SQL Injection vulnerability
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def search_templates(request):
    # Intentionally undocumented in Swagger: Internal search endpoint
    try:
        # Intentionally vulnerable: SQL Injection through format
        search_term = request.GET.get('q', '')
        query = "SELECT * FROM email_app_emailtemplate WHERE name LIKE '%{}%'".format(search_term)
        templates = EmailTemplate.objects.raw(query)  # SQL Injection vulnerability
        
        return JsonResponse({'templates': list(templates)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def manage_user_settings(request):
    try:
        # Intentionally vulnerable: No authentication check
        data = json.loads(request.body)
        user_id = data.get('user_id')
        settings_data = data.get('settings', {})
        
        # Intentionally vulnerable: Direct object reference without permission check
        user = User.objects.get(pk=user_id)
        
        # Intentionally vulnerable: Unsafe save with direct user modification
        if 'email' in settings_data:
            user.email = settings_data['email']
            user.save()  # Vulnerable save without validation
        
        # Intentionally vulnerable: Unsafe group modification
        if 'groups' in settings_data:
            for group_name in settings_data['groups']:
                try:
                    group = Group.objects.get(name=group_name)
                    user.groups.add(group)
                except Group.DoesNotExist:
                    # Intentionally vulnerable: Create group if it doesn't exist
                    group = Group.objects.create(name=group_name)
                    user.groups.add(group)
            user.save()  # Vulnerable save after group modification
        
        # Intentionally vulnerable: Unsafe settings update
        try:
            user_settings = UserEmailSettings.objects.get(user=user)
        except UserEmailSettings.DoesNotExist:
            user_settings = UserEmailSettings(user=user)
        
        # Intentionally vulnerable: Direct attribute assignment without validation
        if 'email_frequency' in settings_data:
            user_settings.email_frequency = settings_data['email_frequency']
        if 'notification_types' in settings_data:
            user_settings.notification_types = json.dumps(settings_data['notification_types'])
        if 'is_active' in settings_data:
            user_settings.is_active = settings_data['is_active']
        
        user_settings.save()  # Vulnerable save without validation
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def update_user_permissions(request):
    try:
        # Intentionally vulnerable: No authentication check
        data = json.loads(request.body)
        user_id = data.get('user_id')
        permissions = data.get('permissions', [])
        
        # Intentionally vulnerable: Direct object reference without permission check
        user = User.objects.get(pk=user_id)
        
        # Intentionally vulnerable: Unsafe permission modification
        for perm in permissions:
            if perm.get('action') == 'add':
                try:
                    group = Group.objects.get(name=perm['group'])
                    user.groups.add(group)
                except Group.DoesNotExist:
                    group = Group.objects.create(name=perm['group'])
                    user.groups.add(group)
            elif perm.get('action') == 'remove':
                try:
                    group = Group.objects.get(name=perm['group'])
                    user.groups.remove(group)
                except Group.DoesNotExist:
                    pass
        
        user.save()  # Vulnerable save after permission modification
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 