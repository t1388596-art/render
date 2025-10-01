#!/usr/bin/env python3
"""
Check if all required templates exist for deployment
"""
import os
from pathlib import Path

def check_templates():
    """Check if all required templates exist"""
    print("🔍 Checking Template Files")
    print("=" * 40)
    
    base_path = Path(__file__).parent
    templates_path = base_path / 'templates'
    
    required_templates = [
        'registration/login.html',
        'accounts/signup.html',
        'base.html',
        'chat/home.html',
        'accounts/profile.html'
    ]
    
    all_exist = True
    
    for template in required_templates:
        template_path = templates_path / template
        if template_path.exists():
            size = template_path.stat().st_size
            print(f"✅ {template} ({size} bytes)")
        else:
            print(f"❌ {template} - MISSING")
            all_exist = False
    
    print("\n" + "=" * 40)
    if all_exist:
        print("🎉 All required templates exist!")
        print("Ready for deployment!")
    else:
        print("💥 Some templates are missing!")
        print("Fix missing templates before deploying.")
    
    return all_exist

if __name__ == "__main__":
    check_templates()