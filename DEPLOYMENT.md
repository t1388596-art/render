# Deployment Guide for Render.com

## Prerequisites
1. Create a Render.com account
2. Push your code to a GitHub repository
3. Have your Euron API key ready

## Render.com Deployment Steps

### 1. Create a Web Service
1. Go to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `hackversity-ai` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn genai_project.wsgi:application`
   - **Instance Type**: `Free` (or higher for production)

### 2. Add Environment Variables
In your Render service settings, add these environment variables:

**Required:**
- `SECRET_KEY`: Generate a new secret key (use Django's get_random_secret_key())
- `EURON_API_KEY`: Your Euron API key
- `DEBUG`: `False`

**Optional:**
- `DJANGO_LOG_LEVEL`: `INFO`
- `ALLOWED_HOSTS`: Additional domains if needed

### 3. Database Setup
1. Create a PostgreSQL database in Render:
   - Click "New +" and select "PostgreSQL"
   - Choose your preferred settings
   - Copy the "External Database URL"
2. Add the database URL to your web service:
   - Go to your web service settings
   - Add environment variable `DATABASE_URL` with the PostgreSQL URL

### 4. Deploy
1. Click "Deploy" in your Render dashboard
2. Monitor the build logs
3. Once deployed, your app will be available at: `https://your-service-name.onrender.com`

## Important Notes

### Security
- Never commit real environment variables to your repository
- Use Render's environment variable settings for sensitive data
- The app is configured with production security settings when DEBUG=False

### Static Files
- Static files are handled by WhiteNoise middleware
- Files are automatically collected during build process
- No additional configuration needed

### Database
- Uses PostgreSQL in production (recommended)
- Automatically migrates database during deployment
- SQLite is used for local development

### Monitoring
- Check Render logs for deployment issues
- Monitor application performance in Render dashboard
- Set up alerts for critical issues

## Local Development
1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies: `pip install -r requirements.txt`
4. Create `.env` file from `.env.example`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Start server: `python manage.py runserver`

## Troubleshooting

### Common Issues
1. **Build fails**: Check that all dependencies are in requirements.txt
2. **Static files not loading**: Ensure STATIC_ROOT is set correctly
3. **Database connection errors**: Verify DATABASE_URL is set correctly
4. **Secret key errors**: Make sure SECRET_KEY environment variable is set

### Logs
- View build logs in Render dashboard
- Use `python manage.py check --deploy` locally to verify settings
- Monitor application logs for runtime issues