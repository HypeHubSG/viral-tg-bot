#!/usr/bin/env python3
"""
Utility script to get Telegram group ID

This script helps you find the ID of a Telegram group for bot configuration.
"""

import asyncio
import os
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def get_group_info():
    """Get information about groups the bot is in"""
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env file")
        print("Please add your bot token to the .env file first.")
        return
    
    bot = Bot(token=bot_token)
    
    try:
        # Get bot info
        bot_info = await bot.get_me()
        print(f"🤖 Bot: @{bot_info.username}")
        print(f"📝 Bot ID: {bot_info.id}")
        print()
        
        # Note: Telegram bots can't get updates about groups they're in
        # without being added to the group first
        print("📋 To get your group ID:")
        print("1. Add this bot to your group")
        print("2. Send a message in the group")
        print("3. Check the bot logs or use @userinfobot")
        print()
        print("🔍 Alternative methods to find group ID:")
        print("• Use @userinfobot in your group")
        print("• Use @RawDataBot in your group")
        print("• Check the URL when you open your group in web.telegram.org")
        print()
        print("📝 Group ID formats:")
        print("• Public groups: @groupname")
        print("• Private groups: -1001234567890")
        print()
        print("💡 Once you have the group ID, add it to your .env file:")
        print("TELEGRAM_GROUP_ID=@your_group_name_or_id")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your bot token is correct.")

async def main():
    """Main function"""
    print("🔍 Telegram Group ID Finder")
    print("=" * 40)
    await get_group_info()

if __name__ == "__main__":
    asyncio.run(main()) 