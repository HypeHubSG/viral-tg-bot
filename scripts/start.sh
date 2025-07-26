#!/bin/bash

# Viral Telegram Bot Start Script

echo "🤖 Starting Viral Telegram Bot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run the deployment script first:"
    echo "  ./scripts/deploy.sh"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it with your configuration."
    exit 1
fi

# Run the bot
echo "🚀 Starting bot..."
python main.py 