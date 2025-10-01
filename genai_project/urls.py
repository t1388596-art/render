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
from chat.emergency_views import health_check, simple_home, database_status

# Try to import custom login view, fallback to default if there are issues
try:
    from accounts.views import CustomLoginView
    custom_login_available = True
except ImportError:
    from django.contrib.auth.views import LoginView as CustomLoginView
    custom_login_available = False

urlpatterns = [
    # Emergency/debugging endpoints (no database required)
    path('health/', health_check, name='health_check'),
    path('db-status/', database_status, name='database_status'),
    path('simple/', simple_home, name='simple_home'),
    
    # Admin and authentication
    path('admin/', admin.site.urls),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('accounts.urls')),
    
    # Main application
    path('chat/', include('chat.urls')),
    path('api/', include('chat.api_urls')),
    
    # Default redirect - use simple home if database issues
    path('', simple_home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)