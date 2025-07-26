#!/usr/bin/env python3
"""
Setup script for Viral Telegram Bot

This script helps set up the bot by:
1. Creating necessary directories
2. Checking dependencies
3. Validating configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_ffmpeg():
    """Check if ffmpeg is installed"""
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

def install_dependencies():
    """Install required dependencies"""
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "data/videos",
        "data/images", 
        "data/logs",
        "data/database"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_config_file():
    """Check if configuration file exists"""
    config_file = ".env"
    if not os.path.exists(config_file):
        print(f"⚠️  Configuration file '{config_file}' not found")
        print("📝 Please create a .env file with the following variables:")
        print("\n" + "="*50)
        with open("config.env.example", "r") as f:
            print(f.read())
        print("="*50)
        return False
    else:
        print(f"✅ Configuration file '{config_file}' found")
        return True

def validate_config():
    """Validate configuration"""
    try:
        from app.config import Config
        Config.validate()
        print("✅ Configuration validation passed")
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Viral Telegram Bot...\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check ffmpeg
    if not check_ffmpeg():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check configuration
    if not check_config_file():
        print("\n📋 Setup incomplete. Please configure your .env file and run setup again.")
        print("💡 You can use 'python scripts/get_group_id.py' to help find your group ID.")
        sys.exit(1)
    
    # Validate configuration
    if not validate_config():
        print("\n📋 Setup incomplete. Please fix configuration issues and run setup again.")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("You can now run the bot with: python main.py")

if __name__ == "__main__":
    main() 