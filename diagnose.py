#!/usr/bin/env python3
"""
Diagnostic script to identify setup issues
Run this to see what's wrong with your environment
"""

import sys
import subprocess

print("=" * 60)
print("Outfevibe Vision AI - Diagnostic Tool")
print("=" * 60)

# Check Python version
print("\n1. Python Version:")
print(f"   {sys.version}")
if sys.version_info < (3, 8):
    print("   ⚠️  WARNING: Python 3.8+ required")
else:
    print("   ✓ Python version OK")

# Check if virtual environment is active
print("\n2. Virtual Environment:")
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("   ✓ Virtual environment is active")
else:
    print("   ⚠️  WARNING: No virtual environment detected")
    print("   Recommendation: Create and activate venv")

# Check required packages
print("\n3. Required Packages:")
required_packages = [
    'flask',
    'flask_cors',
    'cv2',
    'mediapipe',
    'PIL',
    'numpy',
    'sklearn',
    'google.generativeai',
    'dotenv'
]

missing = []
for package in required_packages:
    try:
        if package == 'cv2':
            __import__('cv2')
        elif package == 'PIL':
            __import__('PIL')
        elif package == 'sklearn':
            __import__('sklearn')
        elif package == 'dotenv':
            __import__('dotenv')
        else:
            __import__(package)
        print(f"   ✓ {package}")
    except ImportError:
        print(f"   ✗ {package} - MISSING")
        missing.append(package)

# Check .env file
print("\n4. Configuration:")
import os
if os.path.exists('.env'):
    print("   ✓ .env file exists")
    # Check for API key
    from dotenv import load_dotenv
    load_dotenv()
    if os.getenv('GEMINI_API_KEY'):
        print("   ✓ GEMINI_API_KEY is set")
    else:
        print("   ⚠️  GEMINI_API_KEY not found in .env")
else:
    print("   ✗ .env file not found")
    print("   Recommendation: Copy .env.example to .env and add API key")

# Check uploads directory
print("\n5. Directories:")
if os.path.exists('uploads'):
    print("   ✓ uploads/ directory exists")
else:
    print("   ⚠️  uploads/ directory missing")
    print("   Creating uploads/ directory...")
    os.makedirs('uploads', exist_ok=True)
    print("   ✓ uploads/ directory created")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

if missing:
    print(f"\n❌ {len(missing)} package(s) missing")
    print("\nTo fix, run:")
    print("   pip install -r requirements.txt")
else:
    print("\n✅ All packages installed!")

if not os.path.exists('.env'):
    print("\n⚠️  Configuration needed:")
    print("   1. Copy .env.example to .env")
    print("   2. Add your GEMINI_API_KEY")
elif not os.getenv('GEMINI_API_KEY'):
    print("\n⚠️  Add GEMINI_API_KEY to .env file")

print("\n" + "=" * 60)
