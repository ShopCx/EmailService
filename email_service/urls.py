from django.urls import path, include

urlpatterns = [
    path('api/email/', include('email_app.urls')),
] 