import os
import asyncio
import aiofiles
import yt_dlp
from PIL import Image
import tempfile
from typing import Optional, Tuple
from app.config import Config
from app.utils.logger import logger

class VideoProcessor:
    """Service for processing videos and extracting cover images"""
    
    def __init__(self):
        self.videos_dir = Config.VIDEOS_DIR
        self.images_dir = Config.IMAGES_DIR
        self.max_size_mb = Config.MAX_VIDEO_SIZE_MB
        
        # Create directories if they don't exist
        os.makedirs(self.videos_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
    
    async def download_video(self, file_id: str, file_path: str) -> Optional[str]:
        """Download video from Telegram and save to local storage"""
        try:
            # Generate unique filename
            timestamp = int(asyncio.get_event_loop().time())
            video_filename = f"video_{file_id}_{timestamp}.mp4"
            video_path = os.path.join(self.videos_dir, video_filename)
            
            # Check file size
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if file_size_mb > self.max_size_mb:
                logger.warning(f"Video too large: {file_size_mb:.2f}MB > {self.max_size_mb}MB")
                return None
            
            # Copy file to videos directory
            async with aiofiles.open(file_path, 'rb') as src:
                async with aiofiles.open(video_path, 'wb') as dst:
                    await dst.write(await src.read())
            
            logger.info(f"Video downloaded successfully: {video_path}")
            return video_path
            
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            return None
    
    def extract_cover_image(self, video_path: str) -> Optional[str]:
        """Extract cover image from video using ffmpeg"""
        try:
            # Generate image filename
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            image_filename = f"cover_{video_name}.jpg"
            image_path = os.path.join(self.images_dir, image_filename)
            
            # Use ffmpeg to extract first frame
            import subprocess
            cmd = [
                'ffmpeg', '-i', video_path, 
                '-vframes', '1', 
                '-q:v', '2', 
                '-y',  # Overwrite output file
                image_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(image_path):
                logger.info(f"Cover image extracted: {image_path}")
                return image_path
            else:
                logger.error(f"ffmpeg failed: {result.stderr}")
                return None
                    
        except Exception as e:
            logger.error(f"Error extracting cover image: {e}")
            return None
    
    async def process_video(self, file_id: str, file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """Process video: download and extract cover image"""
        try:
            # Download video
            video_path = await self.download_video(file_id, file_path)
            if not video_path:
                return None, None
            
            # Extract cover image
            image_path = self.extract_cover_image(video_path)
            
            return video_path, image_path
            
        except Exception as e:
            logger.error(f"Error processing video: {e}")
            return None, None
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """Clean up old video and image files"""
        try:
            import time
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            # Clean videos
            for filename in os.listdir(self.videos_dir):
                file_path = os.path.join(self.videos_dir, filename)
                if os.path.isfile(file_path):
                    if current_time - os.path.getmtime(file_path) > max_age_seconds:
                        os.remove(file_path)
                        logger.info(f"Cleaned up old video: {filename}")
            
            # Clean images
            for filename in os.listdir(self.images_dir):
                file_path = os.path.join(self.images_dir, filename)
                if os.path.isfile(file_path):
                    if current_time - os.path.getmtime(file_path) > max_age_seconds:
                        os.remove(file_path)
                        logger.info(f"Cleaned up old image: {filename}")
                        
        except Exception as e:
            logger.error(f"Error cleaning up old files: {e}") 