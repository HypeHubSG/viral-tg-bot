#!/bin/bash

# Viral Telegram Bot Deployment Script

set -e

echo "🚀 Deploying Viral Telegram Bot..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version is installed, but Python $required_version or higher is required."
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/videos data/images data/logs data/database

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Please create a .env file with the following variables:"
    echo ""
    echo "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here"
    echo "TELEGRAM_CHANNEL_ID=@your_channel_username_or_id"
    echo "OPENAI_API_KEY=your_openai_api_key_here"
    echo ""
    echo "You can copy from config.env.example as a starting point."
    exit 1
fi

# Run tests
echo "🧪 Running tests..."
python scripts/test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment completed successfully!"
    echo ""
    echo "To start the bot, run:"
    echo "  source venv/bin/activate"
    echo "  python main.py"
    echo ""
    echo "Or use the start script:"
    echo "  ./scripts/start.sh"
else
    echo "❌ Tests failed. Please check the errors above."
    exit 1
fi 