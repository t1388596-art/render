from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def custom_login_view(request):
    """Production-safe login view with template fallback"""
    from django.contrib.auth import authenticate, login
    from django.contrib.auth.forms import AuthenticationForm
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/chat/')
        error_message = "Invalid username or password"
    else:
        form = CustomAuthenticationForm()
        error_message = ""
    
    # Try to render template, fallback to inline HTML if not found
    try:
        return render(request, 'accounts/login.html', {'form': form})
    except:
            # Fallback to inline template
            html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - GenAI Chat</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 0; min-height: 100vh;
            display: flex; align-items: center; justify-content: center;
        }}
        .login-container {{
            background: white; padding: 2rem; border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 100%; max-width: 400px;
        }}
        .login-header {{ text-align: center; margin-bottom: 2rem; }}
        .login-header h1 {{ color: #333; margin-bottom: 0.5rem; }}
        .form-group {{ margin-bottom: 1rem; }}
        label {{ display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500; }}
        input[type="text"], input[type="password"] {{
            width: 100%; padding: 0.75rem; border: 2px solid #e1e1e1;
            border-radius: 5px; font-size: 1rem; box-sizing: border-box;
        }}
        .btn-primary {{
            width: 100%; padding: 0.75rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; border-radius: 5px; font-size: 1rem; cursor: pointer;
        }}
        .login-links {{ text-align: center; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #e1e1e1; }}
        .login-links a {{ color: #667eea; text-decoration: none; }}
        .error-messages {{ background: #fee; border: 1px solid #fcc; color: #c33; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; }}
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>Welcome Back</h1>
            <p>Sign in to your GenAI Chat account</p>
        </div>
        {('<div class="error-messages"><p>' + error_message + '</p></div>') if error_message else ''}
        <form method="post">
            <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" name="username" id="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" name="password" id="password" required>
            </div>
            <button type="submit" class="btn-primary">Sign In</button>
        </form>
        <div class="login-links">
            <p>Don't have an account? <a href="/accounts/signup/">Sign up here</a></p>
            <p><a href="/">← Back to Home</a></p>
        </div>
    </div>
</body>
</html>
            '''
            return HttpResponse(html_content)


class CustomLoginView(LoginView):
    """Kept for compatibility but will use function view"""
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('chat:home')
    
    def post(self, request, *args, **kwargs):
        """Override post method to handle missing templates gracefully"""
        try:
            return super().post(request, *args, **kwargs)
        except TemplateDoesNotExist:
            # Process form and render fallback template
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.render_fallback_login(request, form)
    
    def render_fallback_login(self, request, form=None):
        """Render inline login template as fallback"""
        if form is None:
            form = self.get_form()
        
        # Inline HTML template for production fallback
        html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - GenAI Chat</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .login-container {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }}
        .login-header {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        .login-header h1 {{
            color: #333;
            margin-bottom: 0.5rem;
        }}
        .form-group {{
            margin-bottom: 1rem;
        }}
        label {{
            display: block;
            margin-bottom: 0.5rem;
            color: #333;
            font-weight: 500;
        }}
        input[type="text"], input[type="password"] {{
            width: 100%;
            padding: 0.75rem;
            border: 2px solid #e1e1e1;
            border-radius: 5px;
            font-size: 1rem;
            box-sizing: border-box;
        }}
        .btn-primary {{
            width: 100%;
            padding: 0.75rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 1rem;
            cursor: pointer;
        }}
        .login-links {{
            text-align: center;
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid #e1e1e1;
        }}
        .login-links a {{
            color: #667eea;
            text-decoration: none;
        }}
        .error-messages {{
            background: #fee;
            border: 1px solid #fcc;
            color: #c33;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
        }}
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>Welcome Back</h1>
            <p>Sign in to your GenAI Chat account</p>
        </div>

        {self.render_form_errors(form)}

        <form method="post">
            <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">
            <div class="form-group">
                <label for="id_username">Username</label>
                <input type="text" name="username" id="id_username" required>
            </div>
            
            <div class="form-group">
                <label for="id_password">Password</label>
                <input type="password" name="password" id="id_password" required>
            </div>

            <button type="submit" class="btn-primary">Sign In</button>
        </form>

        <div class="login-links">
            <p>Don't have an account? <a href="/accounts/signup/">Sign up here</a></p>
            <p><a href="/">← Back to Home</a></p>
        </div>
    </div>
</body>
</html>
        '''
        
        return HttpResponse(html_content)
    
    def render_form_errors(self, form):
        """Render form errors as HTML string"""
        if not form.errors:
            return ''
        
        error_html = '<div class="error-messages">'
        for field, errors in form.errors.items():
            for error in errors:
                error_html += f'<p>{error}</p>'
        error_html += '</div>'
        return error_html


def custom_signup_view(request):
    """Production-safe signup view with proper form handling"""
    from django.contrib.auth import get_user_model
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('/chat/')
            except Exception as e:
                form.add_error(None, f"Registration failed: {str(e)}")
    else:
        form = CustomUserCreationForm()
    
    # Try to render template with form, fallback to inline HTML if not found
    try:
        return render(request, 'accounts/signup.html', {'form': form})
    except:
        # Fallback to inline template with proper form handling
        csrf_token = request.META.get('CSRF_COOKIE', '')
        if hasattr(request, 'META') and 'HTTP_X_CSRFTOKEN' in request.META:
            csrf_token = request.META['HTTP_X_CSRFTOKEN']
        
        # Get form errors
        error_html = ""
        if form.errors:
            error_html = '<div class="error-messages">'
            for field, errors in form.errors.items():
                for error in errors:
                    error_html += f'<p>{error}</p>'
            error_html += '</div>'
        
        # Get form field values
        username_value = form.data.get('username', '') if form.data else ''
        email_value = form.data.get('email', '') if form.data else ''
        first_name_value = form.data.get('first_name', '') if form.data else ''
        last_name_value = form.data.get('last_name', '') if form.data else ''
        
        html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up - GenAI Chat</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 0; min-height: 100vh;
            display: flex; align-items: center; justify-content: center;
        }}
        .signup-container {{
            background: white; padding: 2rem; border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 100%; max-width: 450px;
        }}
        .signup-header {{ text-align: center; margin-bottom: 2rem; }}
        .signup-header h1 {{ color: #333; margin-bottom: 0.5rem; font-size: 2rem; }}
        .form-group {{ margin-bottom: 1rem; }}
        .form-row {{ display: flex; gap: 1rem; }}
        .form-row .form-group {{ flex: 1; }}
        label {{ display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500; }}
        input[type="text"], input[type="email"], input[type="password"] {{
            width: 100%; padding: 0.75rem; border: 2px solid #e1e1e1;
            border-radius: 5px; font-size: 1rem; box-sizing: border-box;
            transition: border-color 0.3s;
        }}
        input[type="text"]:focus, input[type="email"]:focus, input[type="password"]:focus {{
            outline: none; border-color: #667eea;
        }}
        .btn-primary {{
            width: 100%; padding: 0.75rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; border-radius: 5px; font-size: 1rem; cursor: pointer;
            transition: transform 0.2s; margin-top: 0.5rem;
        }}
        .btn-primary:hover {{ transform: translateY(-2px); }}
        .signup-links {{ text-align: center; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #e1e1e1; }}
        .signup-links a {{ color: #667eea; text-decoration: none; }}
        .signup-links a:hover {{ text-decoration: underline; }}
        .error-messages {{ background: #fee; border: 1px solid #fcc; color: #c33; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; }}
        .help-text {{ font-size: 0.875rem; color: #666; margin-top: 0.25rem; }}
        .required {{ color: #c33; }}
    </style>
</head>
<body>
    <div class="signup-container">
        <div class="signup-header">
            <h1>Join GenAI Chat</h1>
            <p>Create your account to get started</p>
        </div>
        {error_html}
        <form method="post">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <div class="form-group">
                <label for="id_username">Username <span class="required">*</span></label>
                <input type="text" name="username" id="id_username" value="{username_value}" placeholder="Username" required>
            </div>
            <div class="form-group">
                <label for="id_email">Email Address <span class="required">*</span></label>
                <input type="email" name="email" id="id_email" value="{email_value}" placeholder="Email address" required>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="id_first_name">First Name</label>
                    <input type="text" name="first_name" id="id_first_name" value="{first_name_value}" placeholder="First name (optional)">
                </div>
                <div class="form-group">
                    <label for="id_last_name">Last Name</label>
                    <input type="text" name="last_name" id="id_last_name" value="{last_name_value}" placeholder="Last name (optional)">
                </div>
            </div>
            <div class="form-group">
                <label for="id_password1">Password <span class="required">*</span></label>
                <input type="password" name="password1" id="id_password1" placeholder="Password" required>
                <div class="help-text">Your password must contain at least 8 characters.</div>
            </div>
            <div class="form-group">
                <label for="id_password2">Confirm Password <span class="required">*</span></label>
                <input type="password" name="password2" id="id_password2" placeholder="Confirm password" required>
            </div>
            <button type="submit" class="btn-primary">Create Account</button>
        </form>
        <div class="signup-links">
            <p>Already have an account? <a href="/accounts/login/">Sign in here</a></p>
            <p><a href="/simple/">← Back to Home</a></p>
        </div>
    </div>
</body>
</html>
        '''
        return HttpResponse(html_content)


class SignUpView(CreateView):
    """Kept for compatibility but will use function view"""
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('chat:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        # Notification removed per user request
        return response


@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })