import os
import tempfile
from typing import Optional
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from app.config import Config
from app.services.video_processor import VideoProcessor
from app.services.ai_analyzer import AIAnalyzer
from app.utils.logger import logger

class ViralTelegramBot:
    """Main Telegram bot class for viral video analysis"""
    
    def __init__(self):
        self.config = Config
        self.video_processor = VideoProcessor()
        self.ai_analyzer = AIAnalyzer()
        self.application = Application.builder().token(self.config.TELEGRAM_BOT_TOKEN).build()
        
        # Validate configuration
        self.config.validate()
        
        # Add message handler for videos (higher priority)
        self.application.add_handler(
            MessageHandler(filters.VIDEO, self.handle_video_message)
        )
        # Add message handler for video notes
        self.application.add_handler(
            MessageHandler(filters.VIDEO_NOTE, self.handle_video_message)
        )
        # Add message handler for documents (video files)
        self.application.add_handler(
            MessageHandler(filters.Document.VIDEO, self.handle_video_message)
        )
        
        # Add message handler for ALL other messages (for debugging) - lower priority
        self.application.add_handler(
            MessageHandler(filters.ALL, self.handle_all_messages)
        )

    async def handle_all_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all messages for debugging"""
        try:
            message = update.message
            chat_id = message.chat_id
            
            # Get message type correctly
            message_type = "unknown"
            if message.text:
                message_type = "text"
            elif message.video:
                message_type = "video"
            elif message.photo:
                message_type = "photo"
            elif message.document:
                message_type = "document"
            elif message.audio:
                message_type = "audio"
            elif message.voice:
                message_type = "voice"
            elif message.video_note:
                message_type = "video_note"
            
            logger.info(f"🔍 DEBUG: Received {message_type} message in chat: {chat_id}")
            logger.info(f"🔍 DEBUG: Message: {message}")
            logger.info(f"🔍 DEBUG: Target group ID: {self.config.TELEGRAM_GROUP_ID}")
            
            if hasattr(message.chat, 'title'):
                logger.info(f"🔍 DEBUG: Chat title: {message.chat.title}")
            if hasattr(message.chat, 'username'):
                logger.info(f"🔍 DEBUG: Chat username: {message.chat.username}")
                
        except Exception as e:
            logger.error(f"Error in handle_all_messages: {e}")

    async def handle_video_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            message = update.message
            chat_id = message.chat_id
            
            logger.info(f"🎬 VIDEO HANDLER: Processing video message in chat: {chat_id}")
            logger.info(f"🎬 VIDEO HANDLER: Target group ID: {self.config.TELEGRAM_GROUP_ID}")
            
            if hasattr(message.chat, 'title'):
                logger.info(f"🎬 VIDEO HANDLER: Chat title: {message.chat.title}")
            if hasattr(message.chat, 'username'):
                logger.info(f"🎬 VIDEO HANDLER: Chat username: {message.chat.username}")
            # Check if message is from the target group
            target_group_id = self.config.TELEGRAM_GROUP_ID
            logger.info(f"🎬 DEBUG: Comparing chat_id '{chat_id}' with target_group_id '{target_group_id}'")
            
            # Check if target_group_id is numeric (starts with -)
            if target_group_id.startswith('-'):
                logger.info(f"🎬 DEBUG: Using numeric comparison: '{str(chat_id)}' == '{target_group_id}'")
                if str(chat_id) != target_group_id:
                    logger.info(f"Ignoring message from non-target group: {chat_id}")
                    return
            else:
                logger.info(f"🎬 DEBUG: Using username comparison")
                group_username = target_group_id.replace('@', '')
                if not hasattr(message.chat, 'username') or message.chat.username != group_username:
                    logger.info(f"Ignoring message from non-target group: {chat_id}")
                    return
            logger.info(f"Processing video message from group: {chat_id}")
            logger.info(f"Group title: {message.chat.title if hasattr(message.chat, 'title') else 'Unknown'}")
            # Get video file
            video_file = None
            video_info = {}
            if message.video:
                video_file = message.video
                video_info = {
                    'duration': video_file.duration,
                    'file_size': video_file.file_size,
                    'width': video_file.width,
                    'height': video_file.height
                }
            elif message.video_note:
                video_file = message.video_note
                video_info = {
                    'duration': video_file.duration,
                    'file_size': video_file.file_size
                }
            elif message.document and message.document.mime_type and 'video' in message.document.mime_type:
                video_file = message.document
                video_info = {
                    'file_size': video_file.file_size
                }
            if not video_file:
                logger.warning("No video file found in message")
                return
            # Send processing message
            processing_msg = await context.bot.send_message(
                chat_id=chat_id,
                text="🔄 Processing video... Please wait."
            )
            try:
                # Download video file
                file_path = await self.download_telegram_file(video_file, context.bot)
                if not file_path:
                    await self.update_processing_message(context.bot, processing_msg, "❌ Failed to download video file.")
                    return
                # Process video
                video_path, image_path = await self.video_processor.process_video(
                    str(video_file.file_id), file_path
                )
                if not video_path or not image_path:
                    await self.update_processing_message(context.bot, processing_msg, "❌ Failed to process video or extract cover image.")
                    return
                # Analyze with AI
                await self.update_processing_message(context.bot, processing_msg, "🤖 Analyzing video content...")
                analysis_result = await self.ai_analyzer.get_video_insights(image_path, video_info)
                if not analysis_result:
                    await self.update_processing_message(context.bot, processing_msg, "❌ Failed to analyze video content.")
                    return
                # Send analysis result
                await self.update_processing_message(context.bot, processing_msg, analysis_result)
                logger.info(f"Successfully processed video: {video_file.file_id}")
            except Exception as e:
                logger.error(f"Error processing video message: {e}")
                await self.update_processing_message(context.bot, processing_msg, f"❌ Error processing video: {str(e)}")
            finally:
                if 'file_path' in locals() and os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.error(f"Error handling video message: {e}")

    async def download_telegram_file(self, file, bot) -> Optional[str]:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                file_path = tmp_file.name
            file_obj = await bot.get_file(file.file_id)
            await file_obj.download_to_drive(file_path)
            logger.info(f"Downloaded file to: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error downloading Telegram file: {e}")
            return None

    async def update_processing_message(self, bot, message, new_text: str):
        try:
            await bot.edit_message_text(
                chat_id=message.chat_id,
                message_id=message.message_id,
                text=new_text,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error updating processing message: {e}") 