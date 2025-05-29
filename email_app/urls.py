from django.urls import path
from . import views

urlpatterns = [
    path('send', views.send_email, name='send_email'),
    path('bulk', views.send_bulk_email, name='send_bulk_email'),
    path('template', views.send_template_email, name='send_template_email'),
    path('status', views.get_email_status, name='get_email_status'),
    path('validate', views.validate_email, name='validate_email'),
    path('templates/create', views.create_template, name='create_template'),
    path('templates/search', views.search_templates, name='search_templates'),
    path('user/settings', views.manage_user_settings, name='manage_user_settings'),
    path('user/permissions', views.update_user_permissions, name='update_user_permissions'),
] 