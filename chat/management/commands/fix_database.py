from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
import os


class Command(BaseCommand):
    help = 'Fix database connection issues and setup database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force-sqlite',
            action='store_true',
            help='Force use of SQLite database',
        )

    def handle(self, *args, **options):
        """Fix database connection issues"""
        self.stdout.write(self.style.SUCCESS('🔧 Database Connection Fixer'))
        self.stdout.write('=' * 50)
        
        if options['force_sqlite']:
            self.force_sqlite_mode()
            return
        
        # Check current database configuration
        self.check_current_database()
        
        # Test database connection
        if self.test_database_connection():
            self.stdout.write(self.style.SUCCESS('✅ Database connection is working'))
            
            # Run migrations
            self.run_migrations()
            
            # Create superuser if needed
            self.create_superuser_if_needed()
        else:
            self.stdout.write(self.style.ERROR('❌ Database connection failed'))
            self.suggest_fixes()

    def check_current_database(self):
        """Check current database configuration"""
        self.stdout.write(self.style.HTTP_INFO('\n📊 Current Database Configuration:'))
        
        db_config = settings.DATABASES['default']
        engine = db_config['ENGINE']
        name = db_config['NAME']
        
        if 'postgresql' in engine:
            self.stdout.write(f'  Engine: PostgreSQL')
            self.stdout.write(f'  Host: {db_config.get("HOST", "Not set")}')
            self.stdout.write(f'  Port: {db_config.get("PORT", "Not set")}')
            self.stdout.write(f'  Database: {name}')
        elif 'sqlite' in engine:
            self.stdout.write(f'  Engine: SQLite')
            self.stdout.write(f'  Database file: {name}')
        
        # Check environment variables
        database_url = os.getenv('DATABASE_URL')
        self.stdout.write(f'  DATABASE_URL: {"SET" if database_url else "NOT SET"}')

    def test_database_connection(self):
        """Test database connection"""
        self.stdout.write(self.style.HTTP_INFO('\n🔍 Testing Database Connection:'))
        
        try:
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS('  ✅ Connection successful'))
            
            # Test a simple query
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                self.stdout.write(self.style.SUCCESS(f'  ✅ Query test successful: {result}'))
            
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Connection failed: {e}'))
            return False

    def run_migrations(self):
        """Run database migrations"""
        self.stdout.write(self.style.HTTP_INFO('\n🔄 Running Migrations:'))
        
        from django.core.management import call_command
        
        try:
            call_command('migrate', '--no-input', verbosity=1)
            self.stdout.write(self.style.SUCCESS('  ✅ Migrations completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Migrations failed: {e}'))

    def create_superuser_if_needed(self):
        """Create superuser if none exists"""
        self.stdout.write(self.style.HTTP_INFO('\n👤 Checking Superuser:'))
        
        from django.contrib.auth import get_user_model
        
        try:
            User = get_user_model()
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123'
                )
                self.stdout.write(self.style.SUCCESS('  ✅ Superuser created: admin/admin123'))
            else:
                self.stdout.write(self.style.SUCCESS('  ✅ Superuser already exists'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Could not create superuser: {e}'))

    def force_sqlite_mode(self):
        """Force application to use SQLite"""
        self.stdout.write(self.style.WARNING('🔄 Forcing SQLite mode...'))
        
        # This would require modifying settings, which is not ideal
        # Instead, provide instructions
        self.stdout.write(self.style.WARNING('To force SQLite mode:'))
        self.stdout.write('1. Remove or comment out DATABASE_URL environment variable')
        self.stdout.write('2. Restart the application')
        self.stdout.write('3. The app will automatically use SQLite')

    def suggest_fixes(self):
        """Suggest fixes for database connection issues"""
        self.stdout.write(self.style.WARNING('\n🔧 Suggested Fixes:'))
        self.stdout.write('1. Check if PostgreSQL database is running and accessible')
        self.stdout.write('2. Verify DATABASE_URL environment variable is correct')
        self.stdout.write('3. Check network connectivity between services')
        self.stdout.write('4. Try restarting both database and web service')
        self.stdout.write('5. Use --force-sqlite flag to temporarily use SQLite')
        
        self.stdout.write(self.style.HTTP_INFO('\n🌐 For Render.com:'))
        self.stdout.write('1. Ensure database service is created and running')
        self.stdout.write('2. Copy the Internal Database URL (not External)')
        self.stdout.write('3. Set DATABASE_URL environment variable in web service')
        self.stdout.write('4. Make sure both services are in the same region')
        self.stdout.write('5. Check Render dashboard for service status')