#!/usr/bin/env python3
"""
Standalone database connection tester for Render.com deployment
Run this to test database connectivity without Django overhead
"""
import os
import sys

def test_database_connection():
    """Test database connection directly"""
    print("🔍 Standalone Database Connection Test")
    print("=" * 50)
    
    # Check for DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        print("💡 This means you're using SQLite (local file)")
        return False
    
    print(f"✅ DATABASE_URL is set")
    
    # Parse DATABASE_URL
    try:
        if 'postgresql://' not in database_url:
            print("❌ DATABASE_URL is not a PostgreSQL URL")
            return False
        
        print("✅ DATABASE_URL is PostgreSQL format")
        
        # Extract components
        import re
        
        # Extract hostname
        hostname_match = re.search(r'@([^:]+)', database_url)
        if hostname_match:
            hostname = hostname_match.group(1)
            print(f"📡 Hostname: {hostname}")
            
            # Check hostname format
            if hostname.endswith('.render.com'):
                print("✅ Using Internal Database URL (correct)")
            elif hostname.endswith('-a'):
                print("⚠️  Using External Database URL (this won't work)")
                print("🔧 Fix: Use Internal Database URL instead")
                return False
            else:
                print(f"⚠️  Unknown hostname format: {hostname}")
        
        # Try to connect
        print("\n🧪 Testing actual connection...")
        
        try:
            import psycopg2
            from urllib.parse import urlparse
            
            # Parse the URL
            parsed = urlparse(database_url)
            
            conn = psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port or 5432,
                user=parsed.username,
                password=parsed.password,
                dbname=parsed.path.lstrip('/'),
                connect_timeout=10
            )
            
            print("✅ Database connection successful!")
            
            # Test a simple query
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"📊 PostgreSQL version: {version[0][:50]}...")
            
            cursor.close()
            conn.close()
            
            return True
            
        except ImportError:
            print("❌ psycopg2 not installed - cannot test PostgreSQL connection")
            return False
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            
            # Provide specific guidance based on error
            error_str = str(e).lower()
            if 'could not translate host name' in error_str:
                print("\n🚨 HOSTNAME RESOLUTION ERROR:")
                print("This usually means you're using External Database URL")
                print("🔧 Solution: Switch to Internal Database URL")
            elif 'connection refused' in error_str:
                print("\n🚨 CONNECTION REFUSED:")
                print("Database might be down or not accessible")
            elif 'timeout' in error_str:
                print("\n🚨 CONNECTION TIMEOUT:")
                print("Network issues or database overloaded")
            
            return False
            
    except Exception as e:
        print(f"❌ Error parsing DATABASE_URL: {e}")
        return False

def main():
    """Main function"""
    success = test_database_connection()
    
    if success:
        print("\n🎉 Database connection test PASSED!")
        print("Your PostgreSQL database is properly configured.")
    else:
        print("\n💥 Database connection test FAILED!")
        print("Check the recommendations above to fix the issue.")
        print("\n📋 Quick fixes to try:")
        print("1. Use Internal Database URL (not External)")
        print("2. Verify both services are in same Render region") 
        print("3. Check database service is running")
        print("4. Restart both database and web services")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())