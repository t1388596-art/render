#!/usr/bin/env python3
"""
Test script to verify Euron API integration
"""
import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

def test_euron_api():
    """Test the Euron API directly"""
    print("🔍 Testing Euron API...")
    
    api_key = os.getenv('EURON_API_KEY')
    if not api_key:
        print("❌ EURON_API_KEY not found in environment variables")
        print("📝 Please add your API key to the .env file")
        return False
    
    if api_key == 'YOUR_API_KEY':
        print("⚠️  Please replace YOUR_API_KEY with your actual Euron API key")
        return False
    
    print("✅ API key is configured")
    
    # Test API connection
    test_api = input("🤔 Do you want to test the API connection? (y/n): ").lower().strip()
    
    if test_api == 'y':
        try:
            url = "https://api.euron.one/api/v1/euri/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "messages": [{"role": "user", "content": "Hello!"}],
                "model": "gpt-4.1-nano"
            }
            
            print("📡 Making API request...")
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                response_data = response.json()
                print("✅ API connection successful!")
                
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    ai_response = response_data['choices'][0]['message']['content']
                    print(f"🤖 AI Response: {ai_response}")
                else:
                    print(f"📄 Full response: {json.dumps(response_data, indent=2)}")
                
                return True
            else:
                print(f"❌ API request failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API connection failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    else:
        print("⏭️  Skipping API connection test")
        return True

def test_django_integration():
    """Test Django integration with Euron API"""
    print("\n🧪 Testing Django integration...")
    
    try:
        # Set up Django environment
        os.environ['DJANGO_SETTINGS_MODULE'] = 'genai_project.settings'
        import django
        django.setup()
        
        from chat.services import AIService
        
        ai_service = AIService()
        
        if not ai_service.api_key:
            print("⚠️  API key not configured in Django settings")
            return False
        
        print("✅ Django AI service initialized")
        
        # Test response generation
        test_message = "Hello! How are you?"
        print(f"💬 Testing with message: '{test_message}'")
        
        response = ai_service.generate_response(test_message)
        print(f"🤖 AI Response: {response}")
        
        # Test conversation title generation
        title = ai_service.generate_conversation_title(test_message)
        print(f"📝 Generated title: '{title}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Django integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🌐 Euron API Integration Test")
    print("=" * 40)
    
    api_success = test_euron_api()
    django_success = test_django_integration()
    
    if api_success and django_success:
        print("\n🎉 Euron API is ready to use in your Django app!")
        print("💬 You can now chat with the AI in your application")
        print("🚀 Start your Django server with: python manage.py runserver")
    else:
        print("\n❌ Please fix the issues above before using AI features")
        print("🔄 The app will use fallback responses until Euron API is properly configured")