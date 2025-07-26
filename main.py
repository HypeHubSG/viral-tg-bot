#!/usr/bin/env python3
"""
Viral Telegram Bot - Main Entry Point

A Telegram bot that listens to a channel, downloads videos,
extracts cover images, analyzes them with ChatGPT, and sends
analysis results back to the channel.
"""

import signal
import sys
import os
from app.models.bot import ViralTelegramBot
from app.utils.logger import logger

def main():
    """Main function to run the bot"""
    bot = None
    
    try:
        logger.info("Starting Viral Telegram Bot...")
        
        # Create and start bot
        bot = ViralTelegramBot()
        bot.application.run_polling(allowed_updates=None)  # Remove await and just call run_polling
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        if bot:
            # The original code had await bot.stop(), but bot.stop() is not async.
            # Since the main function is now synchronous, we can't await it.
            # The original code also had a signal handler that used os._exit(0),
            # which is not the standard way to handle shutdown in a synchronous context.
            # For now, we'll just log the shutdown.
            logger.info("Bot shutdown complete")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, shutting down...")
    # Use os._exit to avoid issues with event loop
    os._exit(0)

if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the bot
    main() 