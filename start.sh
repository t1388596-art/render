#!/usr/bin/env bash
# Startup script for Render.com deployment
# This runs after the build and before the main application starts

echo "🚀 Starting Django application..."

# Wait a moment for database to be fully ready
echo "⏳ Waiting for database to be ready..."
sleep 5

# Run migrations (this is crucial for first deployment)
echo "🔄 Running database migrations..."
python manage.py migrate --no-input

# Create superuser if it doesn't exist (optional)
echo "👤 Creating superuser (if needed)..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    try:
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print('Superuser created: admin/admin123')
    except Exception as e:
        print(f'Could not create superuser: {e}')
else:
    print('Superuser already exists')
EOF

echo "✅ Startup completed successfully!"

# Start the main application
echo "🌟 Starting gunicorn server..."
exec gunicorn genai_project.wsgi:application