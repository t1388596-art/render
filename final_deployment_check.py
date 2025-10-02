#!/usr/bin/env python3
"""
Final deployment readiness check for Render.com
"""
import os
import sys
from pathlib import Path

def main():
    print("🚀 Final Deployment Readiness Check")
    print("=" * 50)
    
    all_good = True
    
    # Check critical files
    critical_files = [
        'build.sh',
        'start.sh',
        'requirements.txt',
        'runtime.txt',
        'render.yaml',
        'templates/registration/login.html',
        'templates/accounts/signup.html',
        'genai_project/settings.py',
        'genai_project/urls.py'
    ]
    
    print("📁 Critical Files:")
    for file_path in critical_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MISSING")
            all_good = False
    
    print("\n🔧 Configuration:")
    
    # Check settings
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        # Check middleware
        if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
            print("  ✅ WhiteNoise middleware configured")
        else:
            print("  ❌ WhiteNoise middleware missing")
            all_good = False
        
        # Check static files
        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            print("  ✅ STATIC_ROOT configured")
        else:
            print("  ❌ STATIC_ROOT not configured")
            all_good = False
        
        # Check database fallback
        if 'sqlite' in settings.DATABASES['default']['ENGINE']:
            print("  ✅ SQLite fallback configured")
        
        print("  ✅ Django configuration loaded successfully")
        
    except Exception as e:
        print(f"  ❌ Django configuration error: {e}")
        all_good = False
    
    print("\n🌐 Render.com Checklist:")
    print("  □ PostgreSQL database created in Render")
    print("  □ Internal Database URL copied")
    print("  □ DATABASE_URL environment variable set")
    print("  □ SECRET_KEY environment variable set")
    print("  □ DEBUG=False environment variable set")
    print("  □ EURON_API_KEY environment variable set")
    print("  □ Build Command: ./build.sh")
    print("  □ Start Command: ./start.sh")
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 ALL CHECKS PASSED!")
        print("Your application is ready for Render.com deployment!")
        print("\nNext steps:")
        print("1. git add .")
        print("2. git commit -m 'Ready for production deployment'")
        print("3. git push origin main")
        print("4. Deploy on Render.com")
        return 0
    else:
        print("💥 SOME CHECKS FAILED!")
        print("Fix the issues above before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())