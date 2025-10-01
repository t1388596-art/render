#!/usr/bin/env python
"""
Test script to verify chat UI consistency between new and existing users
"""
import os
import django
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from chat.models import Conversation, Message

User = get_user_model()

def test_ui_consistency():
    """Test that new users and existing users see the same chat UI when accessing chat"""
    
    print("🧪 Testing UI consistency between new and existing users...")
    
    client = Client()
    
    # Create test users
    new_user = User.objects.create_user(
        username='newuser',
        email='newuser@test.com',
        password='testpass123'
    )
    
    existing_user = User.objects.create_user(
        username='existinguser', 
        email='existing@test.com',
        password='testpass123'
    )
    
    # Create conversation for existing user
    conversation = Conversation.objects.create(user=existing_user, title="Test Chat")
    Message.objects.create(
        conversation=conversation,
        content="Hello, this is a test message",
        is_from_user=True
    )
    
    print("✅ Test users created")
    
    # Test 1: Both users accessing home page should see landing page
    print("\n📋 Test 1: Home page access")
    
    client.login(username='newuser', password='testpass123')
    response = client.get(reverse('chat:home'))
    new_user_home_content = response.content.decode()
    
    client.login(username='existinguser', password='testpass123')
    response = client.get(reverse('chat:home'))
    existing_user_home_content = response.content.decode()
    
    # Both should show landing page (hero-section)
    new_user_has_hero = 'hero-section' in new_user_home_content
    existing_user_has_hero = 'hero-section' in existing_user_home_content
    
    print(f"   New user sees landing page: {new_user_has_hero}")
    print(f"   Existing user sees landing page: {existing_user_has_hero}")
    
    # Test 2: Both users accessing chat with force_chat=1 should see chat interface
    print("\n📋 Test 2: Chat page access (force_chat=1)")
    
    client.login(username='newuser', password='testpass123')
    response = client.get(reverse('chat:home') + '?force_chat=1')
    new_user_chat_content = response.content.decode()
    
    client.login(username='existinguser', password='testpass123')
    response = client.get(reverse('chat:home') + '?force_chat=1')
    existing_user_chat_content = response.content.decode()
    
    # Both should show chat interface (chat-container)
    new_user_has_chat = 'chat-container' in new_user_chat_content
    existing_user_has_chat = 'chat-container' in existing_user_chat_content
    
    print(f"   New user sees chat interface: {new_user_has_chat}")
    print(f"   Existing user sees chat interface: {existing_user_has_chat}")
    
    # Test 3: Both should see consistent sidebar elements
    print("\n📋 Test 3: Sidebar consistency")
    
    new_user_has_sidebar = 'sidebar' in new_user_chat_content
    existing_user_has_sidebar = 'sidebar' in existing_user_chat_content
    new_user_has_new_chat_btn = 'new-chat-btn' in new_user_chat_content
    existing_user_has_new_chat_btn = 'new-chat-btn' in existing_user_chat_content
    
    print(f"   New user has sidebar: {new_user_has_sidebar}")
    print(f"   Existing user has sidebar: {existing_user_has_sidebar}")
    print(f"   New user has new chat button: {new_user_has_new_chat_btn}")
    print(f"   Existing user has new chat button: {existing_user_has_new_chat_btn}")
    
    # Test 4: Welcome message consistency
    print("\n📋 Test 4: Welcome message consistency")
    
    new_user_has_welcome = 'Welcome to Hackversity Chat' in new_user_chat_content
    # Existing user might not have welcome message if they have an active conversation
    
    print(f"   New user sees welcome message: {new_user_has_welcome}")
    
    # Summary
    print("\n📊 SUMMARY:")
    print("=" * 50)
    
    home_consistent = new_user_has_hero == existing_user_has_hero
    chat_consistent = new_user_has_chat == existing_user_has_chat  
    sidebar_consistent = (new_user_has_sidebar == existing_user_has_sidebar and 
                         new_user_has_new_chat_btn == existing_user_has_new_chat_btn)
    
    print(f"✅ Home page consistency: {'PASS' if home_consistent else 'FAIL'}")
    print(f"✅ Chat interface consistency: {'PASS' if chat_consistent else 'FAIL'}")
    print(f"✅ Sidebar consistency: {'PASS' if sidebar_consistent else 'FAIL'}")
    
    overall_pass = home_consistent and chat_consistent and sidebar_consistent
    print(f"\n🎯 OVERALL RESULT: {'✅ PASS - UI is consistent!' if overall_pass else '❌ FAIL - UI inconsistencies found'}")
    
    # Cleanup
    new_user.delete()
    existing_user.delete()
    
    return overall_pass

if __name__ == '__main__':
    try:
        test_ui_consistency()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()