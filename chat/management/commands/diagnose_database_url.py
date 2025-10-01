from django.core.management.base import BaseCommand
import os
import re


class Command(BaseCommand):
    help = 'Diagnose DATABASE_URL format and provide specific fixes'

    def handle(self, *args, **options):
        """Diagnose DATABASE_URL issues"""
        self.stdout.write(self.style.SUCCESS('🔍 DATABASE_URL Diagnostic Tool'))
        self.stdout.write('=' * 60)
        
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            self.stdout.write(self.style.ERROR('❌ DATABASE_URL environment variable not set'))
            self.provide_setup_instructions()
            return
        
        self.stdout.write(self.style.SUCCESS('✅ DATABASE_URL is set'))
        
        # Analyze URL format
        self.analyze_url_format(database_url)
        
        # Test parsing
        self.test_url_parsing(database_url)
        
        # Provide recommendations
        self.provide_recommendations(database_url)

    def analyze_url_format(self, database_url):
        """Analyze the DATABASE_URL format"""
        self.stdout.write(self.style.HTTP_INFO('\n📋 URL Format Analysis:'))
        
        # Check basic format
        if not database_url.startswith('postgresql://'):
            self.stdout.write(self.style.ERROR('  ❌ URL should start with "postgresql://"'))
            return
        
        self.stdout.write(self.style.SUCCESS('  ✅ Starts with "postgresql://"'))
        
        # Parse components manually
        try:
            # Remove protocol
            url_without_protocol = database_url[13:]  # Remove 'postgresql://'
            
            # Split user:pass@host:port/db
            if '@' not in url_without_protocol:
                self.stdout.write(self.style.ERROR('  ❌ Missing @ separator (no credentials?)'))
                return
            
            credentials_part, host_db_part = url_without_protocol.split('@', 1)
            
            # Check credentials
            if ':' in credentials_part:
                username, password = credentials_part.split(':', 1)
                self.stdout.write(self.style.SUCCESS(f'  ✅ Username: {username}'))
                self.stdout.write(self.style.SUCCESS('  ✅ Password: [HIDDEN]'))
            else:
                self.stdout.write(self.style.ERROR('  ❌ Invalid credentials format (should be user:pass)'))
            
            # Check host and database
            if '/' not in host_db_part:
                self.stdout.write(self.style.ERROR('  ❌ Missing database name (no / separator)'))
                return
            
            host_port_part, database_name = host_db_part.split('/', 1)
            
            if ':' in host_port_part:
                hostname, port = host_port_part.split(':', 1)
                self.stdout.write(self.style.SUCCESS(f'  ✅ Hostname: {hostname}'))
                try:
                    port_num = int(port)
                    self.stdout.write(self.style.SUCCESS(f'  ✅ Port: {port_num}'))
                except ValueError:
                    self.stdout.write(self.style.ERROR(f'  ❌ Invalid port: {port} (should be number)'))
            else:
                hostname = host_port_part
                self.stdout.write(self.style.SUCCESS(f'  ✅ Hostname: {hostname}'))
                self.stdout.write(self.style.WARNING('  ⚠️  Port: Missing (will default to 5432)'))
            
            self.stdout.write(self.style.SUCCESS(f'  ✅ Database: {database_name}'))
            
            # Check hostname format for Render
            if hostname.endswith('.render.com'):
                self.stdout.write(self.style.SUCCESS('  ✅ Using Internal Database URL (correct for Render)'))
            elif hostname.endswith('-a'):
                self.stdout.write(self.style.WARNING('  ⚠️  Hostname looks like External URL format'))
                self.stdout.write('    Consider using Internal Database URL instead')
            else:
                self.stdout.write(self.style.WARNING(f'  ⚠️  Unknown hostname format: {hostname}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Error analyzing URL: {e}'))

    def test_url_parsing(self, database_url):
        """Test URL parsing with dj_database_url"""
        self.stdout.write(self.style.HTTP_INFO('\n🧪 Testing URL Parsing:'))
        
        try:
            import dj_database_url
            
            parsed = dj_database_url.parse(database_url)
            
            self.stdout.write(self.style.SUCCESS('  ✅ URL parsing successful'))
            
            # Check each component
            components = ['ENGINE', 'HOST', 'PORT', 'USER', 'PASSWORD', 'NAME']
            for component in components:
                value = parsed.get(component)
                if value:
                    if component == 'PASSWORD':
                        self.stdout.write(self.style.SUCCESS(f'    {component}: [HIDDEN]'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'    {component}: {value}'))
                else:
                    if component == 'PORT':
                        self.stdout.write(self.style.WARNING(f'    {component}: Not set (will default to 5432)'))
                    else:
                        self.stdout.write(self.style.ERROR(f'    {component}: Missing!'))
                        
        except ImportError:
            self.stdout.write(self.style.ERROR('  ❌ dj_database_url not available'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Parsing failed: {e}'))

    def provide_recommendations(self, database_url):
        """Provide specific recommendations"""
        self.stdout.write(self.style.WARNING('\n💡 Recommendations:'))
        
        # Check if it's an external URL
        if '@dpg-' in database_url and not database_url.endswith('.render.com/'):
            self.stdout.write(self.style.ERROR('🚨 CRITICAL ISSUE DETECTED:'))
            self.stdout.write('  You appear to be using External Database URL')
            self.stdout.write('')
            self.stdout.write('🔧 SOLUTION:')
            self.stdout.write('  1. Go to your PostgreSQL database in Render dashboard')
            self.stdout.write('  2. Look for "Internal Database URL" section')
            self.stdout.write('  3. Copy the Internal Database URL')
            self.stdout.write('  4. Replace DATABASE_URL environment variable in web service')
            self.stdout.write('  5. Restart the web service')
            self.stdout.write('')
            self.stdout.write('📝 Internal URL should end with:')
            self.stdout.write('   .oregon-postgres.render.com:5432/database_name')
            self.stdout.write('   (or .ohio-postgres.render.com etc. depending on region)')
        
        # Check for missing port
        if ':5432/' not in database_url and not database_url.endswith(':5432/'):
            self.stdout.write('')
            self.stdout.write('⚠️  Port Information:')
            self.stdout.write('  Your DATABASE_URL might be missing the port number')
            self.stdout.write('  PostgreSQL default port is 5432')
            self.stdout.write('  This is usually handled automatically, but check if needed')
        
        self.stdout.write('')
        self.stdout.write('🔄 Next Steps:')
        self.stdout.write('  1. Fix DATABASE_URL format if needed')
        self.stdout.write('  2. Restart your web service')
        self.stdout.write('  3. Check logs for "Database connection successful"')
        self.stdout.write('  4. Test with: python manage.py debug_database')

    def provide_setup_instructions(self):
        """Provide setup instructions for missing DATABASE_URL"""
        self.stdout.write(self.style.WARNING('\n🛠️  Setup Instructions:'))
        self.stdout.write('1. Create PostgreSQL database in Render dashboard')
        self.stdout.write('2. Wait for database to be fully provisioned')
        self.stdout.write('3. Copy the Internal Database URL')
        self.stdout.write('4. Add DATABASE_URL environment variable to web service')
        self.stdout.write('5. Set value to the Internal Database URL')
        self.stdout.write('6. Save and restart web service')