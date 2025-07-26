import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Telegram bot"""
    
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_GROUP_ID = os.getenv('TELEGRAM_GROUP_ID')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # File Paths
    VIDEOS_DIR = os.getenv('VIDEOS_DIR', 'data/videos')
    IMAGES_DIR = os.getenv('IMAGES_DIR', 'data/images')
    LOGS_DIR = os.getenv('LOGS_DIR', 'data/logs')
    
    # Bot Settings
    MAX_VIDEO_SIZE_MB = int(os.getenv('MAX_VIDEO_SIZE_MB', 50))
    SUPPORTED_VIDEO_FORMATS = os.getenv('SUPPORTED_VIDEO_FORMATS', 'mp4,avi,mov,mkv,webm').split(',')
    
    @classmethod
    def validate(cls):
        """Validate that all required configuration is present"""
        required_vars = [
            'TELEGRAM_BOT_TOKEN',
            'TELEGRAM_GROUP_ID', 
            'OPENAI_API_KEY'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True 