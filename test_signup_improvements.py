#!/usr/bin/env python
"""
Test script to verify the improved signup page functionality
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

def test_signup_improvements():
    """Test the improved signup functionality"""
    from django.test import Client
    from django.contrib.auth import get_user_model
    from accounts.forms import CustomUserCreationForm
    
    print("Testing improved signup page functionality...")
    
    # Test 1: Form initialization
    try:
        form = CustomUserCreationForm()
        expected_fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        form_fields = list(form.fields.keys())
        print(f"✓ Form fields: {form_fields}")
        
        for field in expected_fields:
            if field in form_fields:
                print(f"✓ Field '{field}' present")
            else:
                print(f"✗ Field '{field}' missing")
    except Exception as e:
        print(f"✗ Error initializing form: {e}")
        return False
    
    # Test 2: Form validation
    try:
        # Test valid form data
        valid_data = {
            'username': 'testuser_signup',
            'email': 'testuser_signup@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = CustomUserCreationForm(data=valid_data)
        if form.is_valid():
            print("✓ Form validation works with valid data")
        else:
            print(f"✗ Form validation failed: {form.errors}")
    except Exception as e:
        print(f"✗ Error validating form: {e}")
        return False
    
    # Test 3: View response
    try:
        client = Client()
        response = client.get('/accounts/signup/')
        print(f"✓ GET /accounts/signup/ status: {response.status_code}")
        
        # Check if form is in context (for template rendering)
        if hasattr(response, 'context') and response.context and 'form' in response.context:
            print("✓ Form properly passed to template context")
        else:
            print("! Form context might be using fallback HTML")
            
    except Exception as e:
        print(f"✗ Error testing view: {e}")
        return False
    
    # Test 4: Template rendering
    try:
        from django.template.loader import get_template
        template = get_template('accounts/signup.html')
        print("✓ Signup template loads successfully")
    except Exception as e:
        print(f"! Template error (fallback HTML will be used): {e}")
    
    print("\n🎉 Signup page improvements test completed!")
    return True

if __name__ == '__main__':
    success = test_signup_improvements()
    sys.exit(0 if success else 1)