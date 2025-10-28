"""
AI Service for generating high-quality presentation content using OpenAI
"""

import os
import json
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from app.core.logging import app_logger
from app.core.config import settings
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

# Debug: Print env path and check if file exists
print(f"Looking for .env file at: {env_path}")
print(f".env file exists: {env_path.exists()}")

# If API key not found in environment, set it directly from .env file
if not os.getenv("OPENAI_API_KEY") and env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('OPENAI_API_KEY='):
                api_key = line.split('=', 1)[1].strip()
                os.environ['OPENAI_API_KEY'] = api_key
                print(f"Manually loaded API key from .env: {api_key[:10]}...")


class AIService:
    """
    Service for generating presentation content using AI
    """
    
    def __init__(self):
        """Initialize AI service with OpenAI client"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)
            self.model = "gpt-4"  # Use GPT-4 for better quality
        else:
            app_logger.warning("OpenAI API key not found. AI features will be limited.")
            self.client = None
            
    async def enhance_markdown_content(self, markdown_text: str, context: Dict[str, Any] = None) -> str:
        """
        Enhance markdown content with AI-generated insights in Korean
        """
        if not self.client:
            return markdown_text
            
        try:
            prompt = f"""
            다음 내용을 맥킨지 품질의 프레젠테이션으로 개선해주세요:
            
            {markdown_text[:3000]}  # Limit input to avoid token overflow
            
            개선 요구사항:
            1. 한글 유지 (원문이 한글인 경우)
            2. Executive Summary 추가
            3. 각 섹션에 구체적 수치와 데이터 추가
            4. 실행 계획과 타임라인 포함
            5. 핵심 인사이트와 제안사항 강조
            6. MECE 원칙 적용
            
            마크다운 형식을 유지하되, 내용을 크게 개선해주세요.
            각 슬라이드는 5-7개의 핵심 포인트로 구성하세요.
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "당신은 한국 맥킨지의 시니어 컨설턴트입니다. 한글로 고품질 프레젠테이션을 작성하세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=3000
            )
            
            enhanced_content = response.choices[0].message.content
            return enhanced_content
            
        except Exception as e:
            app_logger.error(f"AI enhancement failed: {str(e)}")
            return markdown_text
    
    async def generate_executive_summary(self, content: str) -> str:
        """
        Generate executive summary from content
        """
        if not self.client:
            return "Executive Summary\n\n• Key findings\n• Strategic recommendations\n• Next steps"
            
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a McKinsey consultant creating executive summaries."},
                    {"role": "user", "content": f"Create a concise executive summary for:\n\n{content}"}
                ],
                temperature=0.6,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            app_logger.error(f"Executive summary generation failed: {str(e)}")
            return "Executive Summary\n\n• Key findings\n• Strategic recommendations\n• Next steps"
    
    async def generate_data_insights(self, data: Dict[str, Any]) -> List[str]:
        """
        Generate insights from data
        """
        if not self.client:
            return ["Data shows positive trends", "Further analysis recommended"]
            
        try:
            data_str = json.dumps(data, indent=2)
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data analyst providing McKinsey-level insights."},
                    {"role": "user", "content": f"Generate 3-5 key insights from this data:\n\n{data_str}"}
                ],
                temperature=0.6,
                max_tokens=300
            )
            
            insights = response.choices[0].message.content.split('\n')
            return [insight.strip() for insight in insights if insight.strip()]
            
        except Exception as e:
            app_logger.error(f"Data insights generation failed: {str(e)}")
            return ["Data shows positive trends", "Further analysis recommended"]
    
    async def improve_slide_content(self, slide: Dict[str, Any]) -> Dict[str, Any]:
        """
        Improve individual slide content with Korean language preservation
        """
        if not self.client:
            return slide
            
        try:
            # Optimize content for PPT layout
            content_list = slide.get('content', [])
            if isinstance(content_list, list):
                content_text = '\n'.join(content_list[:10])  # Limit to prevent overflow
            else:
                content_text = str(content_list)[:500]
            
            prompt = f"""
            맥킨지 스타일 프레젠테이션 슬라이드를 개선해주세요.
            
            현재 슬라이드:
            제목: {slide.get('title', '')}
            내용: {content_text}
            
            개선 요구사항:
            1. 한글로 작성 (영어 용어는 필요시만 사용)
            2. 핵심 메시지 3-5개로 요약
            3. 각 포인트는 15단어 이내
            4. 구체적 수치와 데이터 포함
            5. 실행 가능한 제안 포함
            
            JSON 형식으로 응답:
            {{
                "title": "개선된 제목 (20자 이내)",
                "content": ["포인트1 (간결하게)", "포인트2", "포인트3", "최대 5개까지"],
                "speaker_notes": "발표자 노트 (선택사항)"
            }}
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "당신은 한국 맥킨지 컨설턴트입니다. 한글로 간결하고 임팩트 있는 슬라이드를 만드세요. 반드시 유효한 JSON 형식으로 응답하세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,  # Lower for more consistent formatting
                max_tokens=800
            )
            
            response_text = response.choices[0].message.content
            # Clean up response for JSON parsing
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]
                
            improved = json.loads(response_text.strip())
            
            # Ensure content fits in slide layout
            improved_content = improved.get('content', slide.get('content', []))
            if isinstance(improved_content, list):
                # Limit each bullet point length and total number
                improved_content = [str(item)[:100] for item in improved_content[:5]]
            
            slide['title'] = improved.get('title', slide.get('title', ''))[:50]  # Limit title length
            slide['content'] = improved_content
            if 'speaker_notes' in improved:
                slide['speaker_notes'] = improved['speaker_notes']
            
            return slide
            
        except json.JSONDecodeError as e:
            app_logger.error(f"JSON parsing failed: {str(e)}")
            # Return original with length limits
            slide['content'] = slide.get('content', [])[:5] if isinstance(slide.get('content'), list) else []
            return slide
        except Exception as e:
            app_logger.error(f"Slide improvement failed: {str(e)}")
            return slide
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for McKinsey-style content"""
        return """
        You are a senior McKinsey consultant creating high-quality presentations.
        Your content should be:
        
        1. **Data-Driven**: Use specific numbers, percentages, and metrics
        2. **Action-Oriented**: Focus on recommendations and next steps
        3. **Structured**: Use MECE principle (Mutually Exclusive, Collectively Exhaustive)
        4. **Executive-Ready**: Clear, concise, and impactful
        5. **Visual**: Structure content for easy visualization (bullets, charts, matrices)
        
        Style guidelines:
        - Use "So What?" test for every slide
        - Lead with insights, not just data
        - Use pyramid principle for argumentation
        - Include specific recommendations
        - Quantify impact where possible
        """
    
    def _build_enhancement_prompt(self, markdown_text: str, context: Dict[str, Any] = None) -> str:
        """Build prompt for content enhancement"""
        prompt = f"""
        Enhance this presentation content to McKinsey quality standards:
        
        {markdown_text}
        
        Requirements:
        1. Add specific data points and metrics where generic statements exist
        2. Convert observations into actionable insights
        3. Add executive summary if missing
        4. Structure content using MECE principle
        5. Add "So What?" implications for each major point
        6. Include implementation roadmap where applicable
        7. Add risk mitigation strategies
        8. Quantify expected outcomes
        
        Keep the markdown format but improve the content quality significantly.
        """
        
        if context:
            prompt += f"\n\nContext: {json.dumps(context, indent=2)}"
            
        return prompt


class MockAIService(AIService):
    """
    Mock AI Service for testing without API key
    """
    
    def __init__(self):
        """Initialize mock service"""
        self.client = None
        app_logger.info("Using Mock AI Service (no API key configured)")
    
    async def enhance_markdown_content(self, markdown_text: str, context: Dict[str, Any] = None) -> str:
        """Return enhanced mock content"""
        # Add some basic enhancements
        enhanced = markdown_text.replace(
            "## Executive Summary",
            "## Executive Summary\n\n"
            "### Key Findings\n"
            "• Market opportunity valued at $2.3B with 25% CAGR\n"
            "• Digital transformation can reduce operational costs by 35%\n"
            "• Customer satisfaction scores increased by 42% post-implementation\n\n"
            "### Strategic Recommendations\n"
            "1. **Immediate** (0-3 months): Launch pilot program in 3 key markets\n"
            "2. **Short-term** (3-6 months): Scale to 10 markets with proven ROI\n"
            "3. **Long-term** (6-12 months): Full rollout with continuous optimization\n\n"
            "### Expected Impact\n"
            "• Revenue increase: $150M in Year 1\n"
            "• Cost reduction: $45M annually\n"
            "• ROI: 320% over 3 years"
        )
        
        # Add more specific metrics
        enhanced = enhanced.replace(
            "Growth rate:",
            "Growth rate: 16.5% CAGR (2x industry average of 8.2%),"
        )
        
        enhanced = enhanced.replace(
            "Current market size:",
            "Current market size: $2.3T (capturing 15% requires $345B investment),"
        )
        
        return enhanced


def get_ai_service() -> AIService:
    """
    Get AI service instance (real or mock based on API key availability)
    """
    # Re-load environment variables when getting AI service
    env_path = Path(__file__).parent.parent.parent / '.env'
    load_dotenv(env_path, override=True)
    
    api_key = os.getenv("OPENAI_API_KEY")
    app_logger.info(f"Checking for OpenAI API key: {'Found' if api_key else 'Not found'}")
    app_logger.info(f"API key starts with: {api_key[:10] if api_key else 'None'}")
    
    if api_key:
        app_logger.info("Using real AI Service with OpenAI")
        return AIService()
    else:
        app_logger.warning("No API key found, using Mock AI Service")
        return MockAIService()