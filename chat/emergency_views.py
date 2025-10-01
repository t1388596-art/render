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
    html = """
    <!DOCTYPE html>
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
    </html>
    """
    return HttpResponse(html)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def database_status(request):
    """Check database status and provide debugging info"""
    from django.db import connection
    from django.conf import settings
    
    status = {
        'database_url_set': bool(os.getenv('DATABASE_URL')),
        'database_engine': settings.DATABASES['default']['ENGINE'],
        'database_name': settings.DATABASES['default']['NAME'],
        'connection_test': False,
        'error': None,
    }
    
    try:
        connection.ensure_connection()
        status['connection_test'] = True
        status['message'] = 'Database connection successful'
    except Exception as e:
        status['error'] = str(e)
        status['message'] = f'Database connection failed: {e}'
    
    return JsonResponse(status)