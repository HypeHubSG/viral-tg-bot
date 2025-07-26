#!/usr/bin/env python3
"""
Environment Check Script for Viral Telegram Bot

This script checks all dependencies and configuration before running the bot.
Run this before starting the bot to ensure everything is properly set up.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add parent directory to Python path so we can import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    print("🎬 Checking ffmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ ffmpeg is installed")
            return True
        else:
            print("❌ ffmpeg is not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ ffmpeg is not installed")
        print("📦 Please install ffmpeg:")
        print("   Ubuntu/Debian: sudo apt install ffmpeg")
        print("   macOS: brew install ffmpeg")
        print("   Windows: Download from https://ffmpeg.org/download.html")
        return False

def check_python_dependencies():
    """Check if required Python packages are installed"""
    print("📦 Checking Python dependencies...")
    required_packages = [
        ('telegram', 'telegram'),
        ('openai', 'openai'), 
        ('yt-dlp', 'yt_dlp'),
        ('Pillow', 'PIL'),
        ('python-dotenv', 'dotenv'),
        ('requests', 'requests'),
        ('aiofiles', 'aiofiles')
    ]
    
    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name}")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All Python dependencies are installed")
    return True

def check_directories():
    """Check if required directories exist"""
    print("📁 Checking directories...")
    directories = [
        "data/videos",
        "data/images", 
        "data/logs",
        "data/database"
    ]
    
    missing_dirs = []
    for directory in directories:
        if Path(directory).exists():
            print(f"✅ {directory}")
        else:
            print(f"❌ {directory}")
            missing_dirs.append(directory)
    
    if missing_dirs:
        print(f"\n❌ Missing directories: {', '.join(missing_dirs)}")
        print("📁 Create with: python scripts/setup_bot.py")
        return False
    
    print("✅ All required directories exist")
    return True

def check_config_file():
    """Check if configuration file exists"""
    print("⚙️  Checking configuration...")
    config_file = ".env"
    if not os.path.exists(config_file):
        print(f"❌ Configuration file '{config_file}' not found")
        print("📝 Please create a .env file with the following variables:")
        print("\n" + "="*50)
        try:
            with open("config.env.example", "r") as f:
                print(f.read())
        except FileNotFoundError:
            print("TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here")
            print("TELEGRAM_GROUP_ID=@your_group_username_or_id")
            print("OPENAI_API_KEY=your_openai_api_key_here")
        print("="*50)
        return False
    else:
        print(f"✅ Configuration file '{config_file}' found")
        return True

def validate_config():
    """Validate configuration"""
    print("🔍 Validating configuration...")
    try:
        from app.config import Config
        Config.validate()
        print("✅ Configuration validation passed")
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

def check_bot_token():
    """Check if bot token is valid"""
    print("🤖 Checking bot token...")
    try:
        from app.config import Config
        import requests
        
        url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get('ok'):
                print(f"✅ Bot token is valid")
                print(f"   Bot: @{bot_info['result']['username']}")
                return True
            else:
                print("❌ Bot token is invalid")
                return False
        else:
            print("❌ Failed to validate bot token")
            return False
    except Exception as e:
        print(f"❌ Error checking bot token: {e}")
        return False

def check_openai_key():
    """Check if OpenAI API key is valid"""
    print("🤖 Checking OpenAI API key...")
    try:
        from app.config import Config
        import openai
        
        client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        # Try a simple API call
        response = client.models.list()
        print("✅ OpenAI API key is valid")
        return True
    except Exception as e:
        print(f"❌ OpenAI API key validation failed: {e}")
        return False

def main():
    """Main check function"""
    print("🔍 Viral Telegram Bot - Environment Check")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("ffmpeg", check_ffmpeg),
        ("Python Dependencies", check_python_dependencies),
        ("Directories", check_directories),
        ("Configuration File", check_config_file),
        ("Configuration Validation", validate_config),
        ("Bot Token", check_bot_token),
        ("OpenAI API Key", check_openai_key),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error during {name} check: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 CHECK RESULTS:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Your bot is ready to run.")
        print("🚀 Start the bot with: python main.py")
        return True
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. Please fix the issues above.")
        print("💡 Run 'python scripts/setup_bot.py' to fix common issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 