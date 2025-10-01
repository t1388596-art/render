#!/usr/bin/env python3
"""
Database connectivity test script for Render.com deployment debugging
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def test_database_connection():
    """Test database connectivity"""
    print("🔍 Testing database connection...")
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
    django.setup()
    
    from django.db import connection
    from django.core.management.color import no_style
    
    try:
        # Test basic connection
        print("📡 Attempting to connect to database...")
        connection.ensure_connection()
        print("✅ Database connection successful!")
        
        # Test if we can run queries
        print("🔍 Testing database queries...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Query test successful: {result}")
        
        # Check database info
        print("📊 Database information:")
        db_settings = connection.settings_dict
        print(f"  Engine: {db_settings['ENGINE']}")
        print(f"  Name: {db_settings['NAME']}")
        print(f"  Host: {db_settings.get('HOST', 'N/A')}")
        print(f"  Port: {db_settings.get('PORT', 'N/A')}")
        
        # Test migration status
        print("🔄 Checking migration status...")
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if plan:
            print(f"⚠️  {len(plan)} migrations pending")
            for migration, backwards in plan:
                print(f"    - {migration}")
        else:
            print("✅ All migrations applied")
            
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Additional debugging info
        if hasattr(e, 'args'):
            print(f"Error args: {e.args}")
            
        # Check environment variables
        print("\n🔧 Environment variables:")
        db_url = os.getenv('DATABASE_URL')
        if db_url:
            # Don't print the full URL for security
            print(f"  DATABASE_URL: {'SET' if db_url else 'NOT SET'}")
            if 'postgresql://' in db_url:
                print("  Database type: PostgreSQL")
            else:
                print(f"  Database type: {db_url.split('://')[0] if '://' in db_url else 'Unknown'}")
        else:
            print("  DATABASE_URL: NOT SET (will use SQLite)")
            
        return False

if __name__ == "__main__":
    print("🧪 Django Database Connectivity Test")
    print("=" * 40)
    
    success = test_database_connection()
    
    if success:
        print("\n🎉 Database connectivity test passed!")
        sys.exit(0)
    else:
        print("\n💥 Database connectivity test failed!")
        sys.exit(1)