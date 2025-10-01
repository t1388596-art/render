"""genai_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from chat.emergency_views import health_check, simple_home, database_status, emergency_login

# Import production-safe views
try:
    from accounts.views import custom_login_view
except ImportError:
    def custom_login_view(request):
        return HttpResponse("Login temporarily unavailable")

urlpatterns = [
    # Emergency/debugging endpoints (no database required)
    path('health/', health_check, name='health_check'),
    path('db-status/', database_status, name='database_status'),
    path('simple/', simple_home, name='simple_home'),
    path('emergency-login/', emergency_login, name='emergency_login'),
    
    # Admin and authentication
    path('admin/', admin.site.urls),
    path('accounts/login/', custom_login_view, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),  # For signup and profile
    
    # Main application
    path('chat/', include('chat.urls')),
    path('api/', include('chat.api_urls')),
    
    # Default redirect - use simple home if database issues
    path('', simple_home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)