#!/usr/bin/env python3
"""
Test script for Viral Telegram Bot

This script tests various components to ensure everything is working correctly.
"""

import os
import sys
import asyncio
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from app.config import Config
        print("✅ Config module imported")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from app.utils.logger import logger
        print("✅ Logger module imported")
    except Exception as e:
        print(f"❌ Logger import failed: {e}")
        return False
    
    try:
        from app.services.video_processor import VideoProcessor
        print("✅ VideoProcessor module imported")
    except Exception as e:
        print(f"❌ VideoProcessor import failed: {e}")
        return False
    
    try:
        from app.services.ai_analyzer import AIAnalyzer
        print("✅ AIAnalyzer module imported")
    except Exception as e:
        print(f"❌ AIAnalyzer import failed: {e}")
        return False
    
    try:
        from app.models.bot import ViralTelegramBot
        print("✅ ViralTelegramBot module imported")
    except Exception as e:
        print(f"❌ ViralTelegramBot import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration validation"""
    print("\n🔍 Testing configuration...")
    
    try:
        from app.config import Config
        Config.validate()
        print("✅ Configuration validation passed")
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

def test_directories():
    """Test if required directories exist"""
    print("\n🔍 Testing directories...")
    
    required_dirs = [
        "data/videos",
        "data/images",
        "data/logs",
        "data/database"
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ Directory exists: {directory}")
        else:
            print(f"❌ Directory missing: {directory}")
            return False
    
    return True

def test_video_processor():
    """Test video processor initialization"""
    print("\n🔍 Testing video processor...")
    
    try:
        from app.services.video_processor import VideoProcessor
        processor = VideoProcessor()
        print("✅ VideoProcessor initialized successfully")
        return True
    except Exception as e:
        print(f"❌ VideoProcessor initialization failed: {e}")
        return False

def test_ai_analyzer():
    """Test AI analyzer initialization"""
    print("\n🔍 Testing AI analyzer...")
    
    try:
        from app.services.ai_analyzer import AIAnalyzer
        analyzer = AIAnalyzer()
        print("✅ AIAnalyzer initialized successfully")
        return True
    except Exception as e:
        print(f"❌ AIAnalyzer initialization failed: {e}")
        return False

async def test_bot_initialization():
    """Test bot initialization"""
    print("\n🔍 Testing bot initialization...")
    
    try:
        from app.models.bot import ViralTelegramBot
        bot = ViralTelegramBot()
        print("✅ Bot initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Bot initialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Viral Telegram Bot tests...\n")
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Directories", test_directories),
        ("Video Processor", test_video_processor),
        ("AI Analyzer", test_ai_analyzer),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    # Test bot initialization (async)
    try:
        result = asyncio.run(test_bot_initialization())
        if result:
            passed += 1
        else:
            print("❌ Bot initialization test failed")
    except Exception as e:
        print(f"❌ Bot initialization test failed: {e}")
    
    total += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The bot is ready to run.")
        print("Run 'python main.py' to start the bot.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 