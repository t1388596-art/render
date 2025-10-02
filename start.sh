#!/usr/bin/env bash
# Startup script for Render.com deployment
# This runs after the build and before the main application starts

echo "🚀 Starting Django application..."

# Function to test database connectivity and get database type
test_db_connection() {
    python -c "
import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

from django.db import connection
from django.conf import settings

try:
    connection.ensure_connection()
    db_engine = settings.DATABASES['default']['ENGINE']
    if 'postgresql' in db_engine:
        print('Database connection successful - PostgreSQL')
        exit(0)
    elif 'sqlite' in db_engine:
        print('Database connection successful - SQLite')
        exit(2)  # Different exit code for SQLite
    else:
        print('Database connection successful - Unknown')
        exit(0)
except Exception as e:
    print(f'Database connection failed: {e}')
    exit(1)
" 2>/dev/null
}

# Test database connection once
echo "⏳ Checking database configuration..."
echo "🔍 Testing database connection..."

test_db_connection
db_test_result=$?

if [ $db_test_result -eq 0 ]; then
    echo "✅ PostgreSQL database connection successful!"
elif [ $db_test_result -eq 2 ]; then
    echo "✅ SQLite database connection successful!"
    echo "� Note: Using SQLite fallback (data won't persist between deployments)"
    echo "💡 To use PostgreSQL: Set DATABASE_URL environment variable with Internal Database URL"
else
    echo "❌ Database connection failed, but continuing with Django's built-in fallback"
fi

# Run migrations (even if database connection failed, this might work with SQLite fallback)
echo "🔄 Running database migrations..."
if python manage.py migrate --no-input; then
    echo "✅ Migrations completed successfully"
else
    echo "⚠️  Migrations failed - application may not work correctly"
fi

# Create superuser if it doesn't exist (optional)
echo "👤 Creating superuser (if needed)..."
python manage.py shell << 'EOF' || echo "⚠️  Could not create superuser"
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print('✅ Superuser created: admin/admin123')
    else:
        print('✅ Superuser already exists')
except Exception as e:
    print(f'⚠️  Could not create superuser: {e}')
EOF

echo "✅ Startup completed!"

# Start the main application
echo "🌟 Starting gunicorn server..."
exec gunicorn genai_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120