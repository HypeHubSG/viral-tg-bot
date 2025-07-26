import base64
import os
from typing import Optional
from openai import OpenAI
from app.config import Config
from app.utils.logger import logger

class AIAnalyzer:
    """Service for analyzing images using OpenAI's GPT-4 Vision"""
    
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = "gpt-4o"
    
    def encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """Encode image to base64 for OpenAI API"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Error encoding image to base64: {e}")
            return None
    
    async def analyze_image(self, image_path: str) -> Optional[str]:
        """Analyze image using GPT-4 Vision and return analysis"""
        try:
            # Check if image exists
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return None
            
            # Encode image
            base64_image = self.encode_image_to_base64(image_path)
            if not base64_image:
                return None
            
            # Prepare the analysis prompt
            analysis_prompt = """
            Analyze this video cover image and provide a comprehensive analysis including:
            
            1. **Content Description**: What is shown in the image?
            2. **Visual Elements**: Colors, composition, style, quality
            3. **Potential Context**: What type of video this might be (tutorial, entertainment, news, etc.)
            4. **Target Audience**: Who might be interested in this content?
            5. **Viral Potential**: What makes this content potentially engaging or shareable?
            6. **Keywords/Tags**: Suggest relevant tags for categorization
            
            Provide your analysis in a clear, structured format that would be useful for content creators and marketers.
            """
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": analysis_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            analysis = response.choices[0].message.content
            logger.info(f"Image analysis completed successfully")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return None
    
    async def generate_response_message(self, analysis: str, video_info: dict = None) -> str:
        """Generate a formatted response message for Telegram"""
        try:
            if not analysis:
                return "❌ Unable to analyze the video cover image."
            
            # Create a formatted message
            message = "🎬 **Video Analysis Report**\n\n"
            
            # Add video info if available
            if video_info:
                if video_info.get('duration'):
                    message += f"⏱️ **Duration**: {video_info['duration']} seconds\n"
                if video_info.get('file_size'):
                    size_mb = video_info['file_size'] / (1024 * 1024)
                    message += f"📁 **Size**: {size_mb:.2f} MB\n"
                message += "\n"
            
            # Add analysis
            message += analysis
            
            # Add footer
            message += "\n\n🤖 *Analysis powered by GPT-4 Vision*"
            
            return message
            
        except Exception as e:
            logger.error(f"Error generating response message: {e}")
            return "❌ Error generating analysis report."
    
    async def get_video_insights(self, image_path: str, video_info: dict = None) -> Optional[str]:
        """Get comprehensive video insights from cover image"""
        try:
            # Analyze the image
            analysis = await self.analyze_image(image_path)
            if not analysis:
                return None
            
            # Generate formatted response
            response = await self.generate_response_message(analysis, video_info)
            return response
            
        except Exception as e:
            logger.error(f"Error getting video insights: {e}")
            return None 