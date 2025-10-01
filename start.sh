#!/usr/bin/env bash
# Startup script for Render.com deployment
# This runs after the build and before the main application starts

echo "🚀 Starting Django application..."

# Function to test database connectivity
test_db_connection() {
    python -c "
import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

from django.db import connection
try:
    connection.ensure_connection()
    print('Database connection successful')
    exit(0)
except Exception as e:
    print(f'Database connection failed: {e}')
    exit(1)
" 2>/dev/null
}

# Wait and retry database connection
echo "⏳ Waiting for database to be ready..."
max_attempts=10
attempt=1

while [ $attempt -le $max_attempts ]; do
    echo "🔍 Database connection attempt $attempt/$max_attempts..."
    
    if test_db_connection; then
        echo "✅ Database connection successful!"
        break
    else
        if [ $attempt -eq $max_attempts ]; then
            echo "⚠️  Database connection failed after $max_attempts attempts"
            echo "🔄 Application will start with SQLite fallback"
            break
        else
            echo "⏳ Waiting 10 seconds before retry..."
            sleep 10
            attempt=$((attempt + 1))
        fi
    fi
done

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