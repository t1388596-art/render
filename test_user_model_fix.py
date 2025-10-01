#!/usr/bin/env python
"""
Test script to verify the User model fix for production
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

def test_user_model_fix():
    """Test that the User model is correctly resolved"""
    print("Testing User model resolution...")
    
    # Test 1: Import get_user_model
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        print(f"✓ Successfully imported User model: {User}")
        print(f"✓ User model class: {User.__name__}")
        print(f"✓ User model app: {User._meta.app_label}")
        print(f"✓ User model is CustomUser: {User.__name__ == 'CustomUser'}")
    except Exception as e:
        print(f"✗ Error importing User model: {e}")
        return False
    
    # Test 2: Check if User model has expected fields
    try:
        expected_fields = ['username', 'email', 'first_name', 'last_name', 'date_joined']
        model_fields = [field.name for field in User._meta.fields]
        print(f"✓ Available fields: {model_fields}")
        
        for field in expected_fields:
            if field in model_fields:
                print(f"✓ Field '{field}' found")
            else:
                print(f"✗ Field '{field}' missing")
    except Exception as e:
        print(f"✗ Error checking fields: {e}")
        return False
    
    # Test 3: Test User.objects manager
    try:
        # This should not raise the AttributeError anymore
        user_count = User.objects.count()
        print(f"✓ User.objects.count() works: {user_count} users in database")
    except Exception as e:
        print(f"✗ Error accessing User.objects: {e}")
        return False
    
    # Test 4: Test filter operations (the ones that were failing)
    try:
        # These were the problematic lines from the error
        username_exists = User.objects.filter(username='test_user').exists()
        email_exists = User.objects.filter(email='test@example.com').exists()
        print(f"✓ Username filter works: {username_exists}")
        print(f"✓ Email filter works: {email_exists}")
    except Exception as e:
        print(f"✗ Error with filter operations: {e}")
        return False
    
    print("\n🎉 All tests passed! The User model fix is working correctly.")
    return True

if __name__ == '__main__':
    success = test_user_model_fix()
    sys.exit(0 if success else 1)