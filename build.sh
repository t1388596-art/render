#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔨 Starting build process..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files (this doesn't require database)
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

# Check if we can connect to the database before running migrations
echo "🔍 Checking database connectivity..."
if python -c "
import os
import sys
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

from django.db import connection
try:
    connection.ensure_connection()
    print('Database connection successful')
    sys.exit(0)
except Exception as e:
    print(f'Database connection failed: {e}')
    sys.exit(1)
"; then
    echo "✅ Database accessible, running migrations..."
    python manage.py migrate
else
    echo "⚠️  Database not accessible during build. Migrations will run on first startup."
    echo "This is normal for Render.com - the database may not be ready during build."
fi

echo "✅ Build completed successfully!"