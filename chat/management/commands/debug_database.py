from django.core.management.base import BaseCommand
from django.conf import settings
import os
import re


class Command(BaseCommand):
    help = 'Debug database connection issues and provide specific fixes for Render.com'

    def handle(self, *args, **options):
        """Debug database connection issues"""
        self.stdout.write(self.style.SUCCESS('🔍 Database Connection Debugger'))
        self.stdout.write('=' * 60)
        
        # Check environment variables
        self.check_environment_variables()
        
        # Analyze DATABASE_URL
        self.analyze_database_url()
        
        # Test connection
        self.test_database_connection()
        
        # Provide specific recommendations
        self.provide_recommendations()

    def check_environment_variables(self):
        """Check database-related environment variables"""
        self.stdout.write(self.style.HTTP_INFO('\n🔧 Environment Variables:'))
        
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            self.stdout.write(self.style.SUCCESS('  ✅ DATABASE_URL: SET'))
            # Don't print the full URL for security reasons
            if 'postgresql://' in database_url:
                self.stdout.write(self.style.SUCCESS('  ✅ Database Type: PostgreSQL'))
            else:
                self.stdout.write(self.style.WARNING('  ⚠️  Database Type: Unknown'))
        else:
            self.stdout.write(self.style.ERROR('  ❌ DATABASE_URL: NOT SET'))
            self.stdout.write('  This means the app will use SQLite')

    def analyze_database_url(self):
        """Analyze the DATABASE_URL format"""
        self.stdout.write(self.style.HTTP_INFO('\n🔍 DATABASE_URL Analysis:'))
        
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            self.stdout.write(self.style.WARNING('  ⚠️  No DATABASE_URL to analyze'))
            return
        
        # Parse the URL components
        try:
            # Extract hostname from URL
            hostname_match = re.search(r'@([^:]+)', database_url)
            if hostname_match:
                hostname = hostname_match.group(1)
                self.stdout.write(f'  📡 Hostname: {hostname}')
                
                # Check if it looks like an internal or external URL
                if hostname.endswith('.render.com'):
                    self.stdout.write(self.style.SUCCESS('  ✅ Hostname format: Render.com (Good)'))
                elif hostname.endswith('-a'):
                    self.stdout.write(self.style.WARNING('  ⚠️  Hostname format: Internal ID only'))
                    self.stdout.write('  This suggests you might be using External URL')
                else:
                    self.stdout.write(self.style.WARNING(f'  ⚠️  Unknown hostname format: {hostname}'))
            
            # Extract port
            port_match = re.search(r':(\d+)/', database_url)
            if port_match:
                port = port_match.group(1)
                self.stdout.write(f'  🔌 Port: {port}')
                if port == '5432':
                    self.stdout.write(self.style.SUCCESS('  ✅ Port: Standard PostgreSQL'))
                else:
                    self.stdout.write(self.style.WARNING(f'  ⚠️  Port: Non-standard ({port})'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Error parsing URL: {e}'))

    def test_database_connection(self):
        """Test the actual database connection"""
        self.stdout.write(self.style.HTTP_INFO('\n🧪 Connection Test:'))
        
        from django.db import connection
        
        try:
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS('  ✅ Database connection: SUCCESSFUL'))
            
            # Get database info
            db_settings = connection.settings_dict
            engine = db_settings['ENGINE']
            
            if 'postgresql' in engine:
                self.stdout.write(self.style.SUCCESS('  ✅ Using: PostgreSQL'))
                self.stdout.write(f'  📊 Database: {db_settings.get("NAME", "Unknown")}')
                self.stdout.write(f'  🖥️  Host: {db_settings.get("HOST", "Unknown")}')
                self.stdout.write(f'  🔌 Port: {db_settings.get("PORT", "Unknown")}')
            elif 'sqlite' in engine:
                self.stdout.write(self.style.WARNING('  ⚠️  Using: SQLite (Fallback)'))
                self.stdout.write('  This means PostgreSQL connection failed')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Database connection: FAILED'))
            self.stdout.write(f'  Error: {e}')

    def provide_recommendations(self):
        """Provide specific recommendations based on findings"""
        self.stdout.write(self.style.WARNING('\n💡 Recommendations:'))
        
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            self.stdout.write('1. Set DATABASE_URL environment variable in Render dashboard')
            self.stdout.write('2. Use the Internal Database URL from your PostgreSQL service')
            return
        
        # Check if hostname looks like external URL
        if database_url and 'dpg-' in database_url and not database_url.endswith('.render.com'):
            self.stdout.write(self.style.ERROR('🚨 LIKELY ISSUE FOUND:'))
            self.stdout.write('  You appear to be using External Database URL')
            self.stdout.write('')
            self.stdout.write('🔧 SOLUTION:')
            self.stdout.write('1. Go to your PostgreSQL database in Render dashboard')
            self.stdout.write('2. Find "Internal Database URL" (not External)')
            self.stdout.write('3. Copy the Internal URL')
            self.stdout.write('4. Update DATABASE_URL environment variable in web service')
            self.stdout.write('5. Restart the web service')
            self.stdout.write('')
            self.stdout.write('📝 Internal URL should look like:')
            self.stdout.write('   postgresql://user:pass@dpg-xxxx-a.oregon-postgres.render.com/dbname')
            self.stdout.write('   (Note the .oregon-postgres.render.com suffix)')
        
        self.stdout.write('')
        self.stdout.write('🆘 If problems persist:')
        self.stdout.write('1. Check that both database and web service are in same region')
        self.stdout.write('2. Verify database service is running and healthy')
        self.stdout.write('3. Try creating a new database service')
        self.stdout.write('4. Contact Render support if the issue continues')