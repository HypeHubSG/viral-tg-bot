#!/bin/bash

# Viral Telegram Bot Start Script

BOT_PID_FILE="bot.pid"
BOT_LOG_FILE="bot.log"

# Function to check if bot is running
check_bot_status() {
    if [ -f "$BOT_PID_FILE" ]; then
        PID=$(cat "$BOT_PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            return 0  # Bot is running
        else
            # PID file exists but process is dead, clean up
            rm -f "$BOT_PID_FILE"
        fi
    fi
    return 1  # Bot is not running
}

# Function to stop the bot
stop_bot() {
    if check_bot_status; then
        PID=$(cat "$BOT_PID_FILE")
        echo "🛑 Stopping bot (PID: $PID)..."
        kill $PID
        rm -f "$BOT_PID_FILE"
        echo "✅ Bot stopped successfully"
    else
        echo "ℹ️  Bot is not running"
    fi
}

# Function to start the bot
start_bot() {
    if check_bot_status; then
        PID=$(cat "$BOT_PID_FILE")
        echo "⚠️  Bot is already running (PID: $PID)"
        echo "Use './scripts/start.sh stop' to stop it first"
        echo "Or use './scripts/start.sh restart' to restart it"
        exit 1
    fi

    echo "🤖 Starting Viral Telegram Bot..."

    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        echo "❌ Virtual environment not found. Please run the deployment script first:"
        echo "  ./scripts/deploy.sh"
        exit 1
    fi

    # Activate virtual environment
    echo "🔧 Activating virtual environment..."
    source .venv/bin/activate

    # Check if .env file exists
    if [ ! -f ".env" ]; then
        echo "❌ .env file not found. Please create it with your configuration."
        exit 1
    fi

    # Start the bot in background
    echo "🚀 Starting bot in background..."
    nohup python main.py > "$BOT_LOG_FILE" 2>&1 &
    BOT_PID=$!
    echo $BOT_PID > "$BOT_PID_FILE"
    echo "✅ Bot started successfully (PID: $BOT_PID)"
    echo "📝 Logs are being written to: $BOT_LOG_FILE"
    echo "💡 Use './scripts/start.sh status' to check bot status"
    echo "💡 Use './scripts/start.sh logs' to view logs"
}

# Function to restart the bot
restart_bot() {
    echo "🔄 Restarting bot..."
    stop_bot
    sleep 2
    start_bot
}

# Function to show bot status
show_status() {
    if check_bot_status; then
        PID=$(cat "$BOT_PID_FILE")
        echo "✅ Bot is running (PID: $PID)"
        echo "📝 Log file: $BOT_LOG_FILE"
    else
        echo "❌ Bot is not running"
    fi
}

# Function to show logs
show_logs() {
    if [ -f "$BOT_LOG_FILE" ]; then
        echo "📋 Bot logs:"
        tail -f "$BOT_LOG_FILE"
    else
        echo "❌ No log file found"
    fi
}

# Main script logic
case "${1:-start}" in
    "start")
        start_bot
        ;;
    "stop")
        stop_bot
        ;;
    "restart")
        restart_bot
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the bot in background"
        echo "  stop    - Stop the running bot"
        echo "  restart - Stop and restart the bot"
        echo "  status  - Show bot status"
        echo "  logs    - Show bot logs (follow mode)"
        exit 1
        ;;
esac 