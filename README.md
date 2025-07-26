# Viral Telegram Bot

A powerful Telegram bot that automatically analyzes videos posted in a group by:
1. **Listening** to a specified Telegram group
2. **Downloading** videos when they're posted
3. **Extracting** cover images from videos
4. **Analyzing** content using GPT-4 Vision
5. **Sending** detailed analysis reports back to the group

## Features

- 🎬 **Video Processing**: Downloads and processes videos from Telegram
- 🖼️ **Cover Extraction**: Automatically extracts cover images from videos
- 🤖 **AI Analysis**: Uses OpenAI's GPT-4 Vision for comprehensive content analysis
- 📊 **Detailed Reports**: Provides structured analysis including viral potential, target audience, and keywords
- 🔄 **Real-time Processing**: Processes videos as they're posted to the group
- 🧹 **Auto Cleanup**: Automatically cleans up old files to save storage

## Architecture

```
viral-tg-bot/
├── app/
│   ├── config.py          # Configuration management
│   ├── models/
│   │   └── bot.py         # Main bot class
│   ├── services/
│   │   ├── video_processor.py  # Video download & processing
│   │   └── ai_analyzer.py      # AI analysis service
│   └── utils/
│       └── logger.py      # Logging utilities
├── data/
│   ├── videos/            # Downloaded videos
│   ├── images/            # Extracted cover images
│   └── logs/              # Application logs
├── scripts/
│   └── setup_bot.py       # Setup script
├── main.py                # Main entry point
├── requirements.txt       # Python dependencies
└── config.env.example     # Configuration template
```

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- OpenAI API Key
- Access to the target Telegram group
- ffmpeg (for video processing)

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd viral-tg-bot
python scripts/setup_bot.py
```

### 1.1. Install ffmpeg (if not already installed)

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install -y ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use:
```bash
winget install ffmpeg
```

### 2. Configure Environment

Create a `.env` file based on `config.env.example`:

```bash
cp config.env.example .env
```

Edit `.env` with your credentials:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_GROUP_ID=@your_group_username_or_id

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# File Paths (optional - defaults provided)
VIDEOS_DIR=data/videos
IMAGES_DIR=data/images
LOGS_DIR=data/logs

# Bot Settings (optional - defaults provided)
MAX_VIDEO_SIZE_MB=50
SUPPORTED_VIDEO_FORMATS=mp4,avi,mov,mkv,webm
```

### 3. Get Telegram Bot Token

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy the bot token to your `.env` file

### 4. Add Bot to Group

1. Add your bot to the target group
2. Give it permission to read messages (if needed)
3. Note the group ID (e.g., `@groupname` or `-1001234567890`)

If the bot is not able to read messages in the group, you can turn off group privacy by following these steps:

1. Message @BotFather on Telegram
2. Send /mybots
3. Select "ViralAsiaBot"
4. Choose "Bot Settings"
5. Select "Group Privacy"
6. Turn OFF group privacy

### 5. Get OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account and get an API key
3. Add the key to your `.env` file

### 6. Check Environment (Optional but Recommended)

Before running the bot, you can check if everything is set up correctly:

```bash
python scripts/check_env.py
```

This will verify all dependencies, configuration, and API keys.

### 7. Run the Bot

```bash
python main.py
```

## Usage

Once running, the bot will:

1. **Monitor** the specified group for video messages
2. **Download** videos automatically when posted
3. **Process** videos and extract cover images
4. **Analyze** content using GPT-4 Vision
5. **Reply** with detailed analysis reports

### Example Analysis Output

```
🎬 Video Analysis Report

⏱️ Duration: 45 seconds
📁 Size: 12.34 MB

**Content Description**: 
This appears to be a tutorial video showing cooking techniques...

**Visual Elements**: 
Bright, well-lit kitchen setting with professional camera work...

**Potential Context**: 
Educational cooking tutorial or recipe demonstration...

**Target Audience**: 
Home cooks, food enthusiasts, and cooking beginners...

**Viral Potential**: 
Clear step-by-step instructions, appealing visuals...

**Keywords/Tags**: 
#cooking #tutorial #recipe #kitchen #food #education

🤖 Analysis powered by GPT-4 Vision
```

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather | Required |
| `TELEGRAM_GROUP_ID` | Target group ID or username | Required |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `MAX_VIDEO_SIZE_MB` | Maximum video size to process | 50 |
| `SUPPORTED_VIDEO_FORMATS` | Comma-separated video formats | mp4,avi,mov,mkv,webm |

## File Management

The bot automatically manages files:

- **Videos**: Stored in `data/videos/` with unique timestamps
- **Images**: Stored in `data/images/` as extracted covers
- **Logs**: Stored in `data/logs/` with daily rotation
- **Cleanup**: Old files are automatically removed after 24 hours

## Troubleshooting

### Common Issues

1. **"Missing required environment variables"**
   - Check your `.env` file exists and has all required variables

2. **"ffmpeg is not installed or not accessible"**
   - Install ffmpeg: `sudo apt install ffmpeg` (Ubuntu/Debian)
   - Or use: `brew install ffmpeg` (macOS)
   - Or download from [ffmpeg.org](https://ffmpeg.org/download.html) (Windows)

3. **"Bot not responding to videos"**
   - Ensure bot is added to group
   - Verify group ID is correct
   - Check bot has read permissions

4. **"Failed to analyze video content"**
   - Verify OpenAI API key is valid
   - Check API quota/credits
   - Ensure video file is accessible

5. **"Video too large"**
   - Increase `MAX_VIDEO_SIZE_MB` in config
   - Or compress videos before posting

### Environment Check

Run the environment check script to diagnose issues:

```bash
python scripts/check_env.py
```

This will check all dependencies, configuration, and API keys.

### Logs

Check logs in `data/logs/` for detailed error information:

```bash
tail -f data/logs/viral_bot_YYYYMMDD.log
```

## Development

### Project Structure

- `app/models/bot.py` - Main bot logic
- `app/services/video_processor.py` - Video handling
- `app/services/ai_analyzer.py` - AI analysis
- `app/config.py` - Configuration management
- `app/utils/logger.py` - Logging utilities

### Adding Features

1. **New Message Types**: Add handlers in `bot.py`
2. **Custom Analysis**: Modify prompts in `ai_analyzer.py`
3. **File Processing**: Extend `video_processor.py`
4. **Configuration**: Add options to `config.py`

## Security Considerations

- Keep your `.env` file secure and never commit it
- Use environment variables in production
- Regularly rotate API keys
- Monitor bot permissions in channels
- Set appropriate file size limits

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs in `data/logs/`
3. Open an issue on GitHub
4. Check configuration and permissions

---

**Note**: This bot requires appropriate permissions and API access. Ensure compliance with Telegram's and OpenAI's terms of service. 