from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os


@require_http_methods(["GET"])
def health_check(request):
    """Simple health check endpoint that doesn't require database"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Application is running',
        'debug': os.getenv('DEBUG', 'False'),
        'database_url_set': bool(os.getenv('DATABASE_URL')),
    })


@require_http_methods(["GET"])
def simple_home(request):
    """Simple home page that doesn't require authentication or database"""
    
    # Get database status
    from django.conf import settings
    db_engine = settings.DATABASES['default']['ENGINE']
    database_url_set = bool(os.getenv('DATABASE_URL'))
    
    if 'postgresql' in db_engine:
        db_status = "🗄️ Database: PostgreSQL (Production)"
        db_class = "status"
    else:
        db_status = "🗄️ Database: SQLite (Fallback)"
        db_class = "status warning"
    
    # Build HTML with string concatenation to avoid template formatting conflicts
    css_warning = '<div class="status warning">⚠️ Data will not persist between deployments. Set DATABASE_URL for PostgreSQL.</div>' if 'sqlite' in db_engine else ''
    
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>Hackversity AI - GenAI Chat</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 { color: #333; margin-bottom: 20px; }
        .status { 
            background: #e8f5e8; 
            color: #2d5f2d; 
            padding: 15px; 
            border-radius: 5px; 
            margin: 20px 0;
            border-left: 4px solid #4caf50;
        }
        .warning {
            background: #fff3cd;
            color: #856404;
            border-left: 4px solid #ffc107;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px;
            font-weight: 500;
        }
        .btn:hover { background: #0056b3; }
        .info { font-size: 14px; color: #666; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Hackversity AI - GenAI Chat</h1>
        
        <div class="status">
            ✅ Application is running successfully!
        </div>
        
        <p>Welcome to the Hackversity AI chat application. This Django app provides AI-powered conversations using the Euron API.</p>
        
        <div class="''' + db_class + '''">
            ''' + db_status + '''
        </div>
        ''' + css_warning + '''
        
        <div style="margin: 30px 0;">
            <a href="/accounts/login/" class="btn">Login</a>
            <a href="/accounts/signup/" class="btn">Sign Up</a>
            <a href="/health/" class="btn" style="background: #28a745;">Health Check</a>
        </div>
        
        <div class="info">
            <p><strong>Features:</strong></p>
            <ul style="text-align: left; display: inline-block;">
                <li>User authentication and registration</li>
                <li>AI-powered chat interface</li>
                <li>Conversation history management</li>
                <li>REST API endpoints</li>
                <li>Admin interface</li>
            </ul>
        </div>
        
        <div class="info">
            <small>Deployed on Render.com | Django 4.2 | Python 3.13</small>
        </div>
    </div>
</body>
</html>'''
    return HttpResponse(html)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def emergency_login(request):
    """Emergency login view that doesn't require templates"""
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        from django.http import JsonResponse
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Login successful'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        else:
            return JsonResponse({'success': False, 'message': 'Username and password required'})
    
    # GET request - show simple login form
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Emergency Login</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
            input { width: 100%; padding: 10px; margin: 5px 0; }
            button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; }
        </style>
    </head>
    <body>
        <h2>Emergency Login</h2>
        <form method="post">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p><a href="/simple/">← Back to Home</a></p>
    </body>
    </html>
    """
    return HttpResponse(html)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def database_status(request):
    """Check database status and provide debugging info"""
    from django.db import connection
    from django.conf import settings
    import os
    from pathlib import Path
    
    status = {
        'database_url_set': bool(os.getenv('DATABASE_URL')),
        'database_engine': settings.DATABASES['default']['ENGINE'],
        'database_name': settings.DATABASES['default']['NAME'],
        'connection_test': False,
        'error': None,
    }
    
    # Add template debugging info
    base_dir = Path(settings.BASE_DIR)
    templates_dir = base_dir / 'templates'
    
    template_status = {
        'templates_dir_exists': templates_dir.exists(),
        'template_files': {},
    }
    
    # Check critical templates
    critical_templates = [
        'registration/login.html',
        'accounts/signup.html',
        'base.html'
    ]
    
    for template in critical_templates:
        template_path = templates_dir / template
        template_status['template_files'][template] = {
            'exists': template_path.exists(),
            'size': template_path.stat().st_size if template_path.exists() else 0
        }
    
    status['templates'] = template_status
    
    # Database connection test
    try:
        connection.ensure_connection()
        status['connection_test'] = True
        status['message'] = 'Database connection successful'
    except Exception as e:
        status['error'] = str(e)
        status['message'] = f'Database connection failed: {e}'
    
    return JsonResponse(status)