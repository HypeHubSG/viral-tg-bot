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
            
            # Prepare the analysis prompt for 小红书 content generation
            analysis_prompt = """
            你是 sgdaily (新加坡每日推荐) 博主助理，主要工作是写小红书文案。
            
            请分析这个视频封面图片，并生成3-4个不同风格的小红书文案版本。要求：
            
            📝 **文案要求**：
            1. 把英文内容翻译成小红书风格的中文
            2. 要有爆点和话题度，吸引眼球
            3. 每个版本都要有不同的角度和风格
            4. 文案要简洁有力，适合小红书平台
            
            🎯 **互动话题**：
            每个文案后面都要加一个带选项的互动话题，提高互动率
            例如："你们觉得呢？A. 太棒了 B. 一般般 C. 想试试"
            
            🏷️ **话题标签**：
            每个文案后面都要加话题标签，必须包含：
            - #新加坡
            - #新加坡生活  
            - #sgdaily
            - 另外再加5-6个相关话题标签
            
            📱 **格式要求**：
            - 使用多emoji表情
            - 话题标签用井号#开头
            - 分点用emoji区分
            - 文案要分段清晰
            
            请生成3-4个不同版本的文案，每个都要有标题、正文、互动话题和话题标签。
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
        """Generate a formatted response message for Telegram with 小红书 content"""
        try:
            if not analysis:
                return "❌ 无法分析视频封面图片。"
            
            # Create a formatted message
            message = "📱 **小红书文案生成**\n\n"
            message += "🎬 基于视频封面分析，为您生成多个小红书文案版本：\n\n"
            
            # Add video info if available
            if video_info:
                if video_info.get('duration'):
                    message += f"⏱️ 视频时长: {video_info['duration']} 秒\n"
                if video_info.get('file_size'):
                    size_mb = video_info['file_size'] / (1024 * 1024)
                    message += f"📁 文件大小: {size_mb:.2f} MB\n"
                message += "\n"
            
            # Add analysis (小红书文案)
            message += analysis
            
            # Add footer
            message += "\n\n🤖 *由 sgdaily 博主助理生成*"
            
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