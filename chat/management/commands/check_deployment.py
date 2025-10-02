from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Check if the application is ready for deployment'

    def handle(self, *args, **options):
        """Run deployment readiness checks"""
        self.stdout.write(self.style.SUCCESS('🚀 Django GenAI Deployment Readiness Check'))
        self.stdout.write('=' * 50)
        
        # Check environment variables
        self.check_environment_variables()
        
        # Check database configuration
        self.check_database()
        
        # Check static files configuration
        self.check_static_files()
        
        # Check API configuration
        self.check_api_config()
        
        self.stdout.write(self.style.SUCCESS('\n✅ Deployment readiness check completed!'))
        self.stdout.write(self.style.WARNING('Remember to:'))
        self.stdout.write('1. Set environment variables in Render.com dashboard')
        self.stdout.write('2. Connect a PostgreSQL database')
        self.stdout.write('3. Push your code to GitHub and deploy')

    def check_environment_variables(self):
        """Check important environment variables"""
        self.stdout.write(self.style.HTTP_INFO('\n🔧 Environment Variables:'))
        
        # Secret Key
        secret_key = settings.SECRET_KEY
        if secret_key and not secret_key.startswith('django-insecure'):
            self.stdout.write(self.style.SUCCESS('  ✅ SECRET_KEY: Configured'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  SECRET_KEY: Using development key'))
        
        # Debug mode
        debug = settings.DEBUG
        if not debug:
            self.stdout.write(self.style.SUCCESS('  ✅ DEBUG: False (production ready)'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  DEBUG: True (development mode)'))
        
        # Allowed hosts
        allowed_hosts = settings.ALLOWED_HOSTS
        if allowed_hosts and allowed_hosts != ['*']:
            self.stdout.write(self.style.SUCCESS(f'  ✅ ALLOWED_HOSTS: {allowed_hosts}'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  ALLOWED_HOSTS: Not properly configured'))

    def check_database(self):
        """Check database configuration"""
        self.stdout.write(self.style.HTTP_INFO('\n💾 Database Configuration:'))
        
        db_config = settings.DATABASES['default']
        engine = db_config['ENGINE']
        
        if 'postgresql' in engine:
            self.stdout.write(self.style.SUCCESS('  ✅ Using PostgreSQL (production ready)'))
        elif 'sqlite' in engine:
            self.stdout.write(self.style.WARNING('  ⚠️  Using SQLite (development only)'))
        
        # Check for DATABASE_URL
        if os.getenv('DATABASE_URL'):
            self.stdout.write(self.style.SUCCESS('  ✅ DATABASE_URL: Configured'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  DATABASE_URL: Not set (will use SQLite)'))

    def check_static_files(self):
        """Check static files configuration"""
        self.stdout.write(self.style.HTTP_INFO('\n📁 Static Files Configuration:'))
        
        # Static root
        if settings.STATIC_ROOT:
            self.stdout.write(self.style.SUCCESS(f'  ✅ STATIC_ROOT: {settings.STATIC_ROOT}'))
        else:
            self.stdout.write(self.style.ERROR('  ❌ STATIC_ROOT: Not configured'))
        
        # WhiteNoise
        middleware = settings.MIDDLEWARE
        if 'whitenoise.middleware.WhiteNoiseMiddleware' in middleware:
            self.stdout.write(self.style.SUCCESS('  ✅ WhiteNoise: Configured'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  WhiteNoise: Not configured'))
        
        # Static files storage
        storage = getattr(settings, 'STATICFILES_STORAGE', 'default')
        if 'whitenoise' in storage.lower():
            self.stdout.write(self.style.SUCCESS('  ✅ Static storage: WhiteNoise'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  Static storage: Default'))

    def check_api_config(self):
        """Check API configuration"""
        self.stdout.write(self.style.HTTP_INFO('\n🔌 API Configuration:'))
        
        # Euron API Key
        api_key = getattr(settings, 'EURON_API_KEY', None)
        if api_key and api_key.startswith('euri-'):
            self.stdout.write(self.style.SUCCESS('  ✅ EURON_API_KEY: Configured'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  EURON_API_KEY: Not properly configured'))
        
        # REST Framework
        if hasattr(settings, 'REST_FRAMEWORK'):
            self.stdout.write(self.style.SUCCESS('  ✅ Django REST Framework: Configured'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  Django REST Framework: Not configured'))