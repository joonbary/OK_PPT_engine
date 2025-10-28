"""
LLM 클라이언트 구현
Claude-3 Opus와 GPT-4 Turbo 통합
"""

import json
import hashlib
from typing import Optional, Dict, List, Any, Union
from abc import ABC, abstractmethod
import logging
from datetime import datetime
import tiktoken
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import openai
except ImportError:
    openai = None

from app.core.config import settings
from app.db.redis_client import get_redis

logger = logging.getLogger(__name__)

class BaseLLMClient(ABC):
    """LLM 클라이언트 베이스 클래스"""
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """텍스트 생성"""
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """토큰 수 계산"""
        pass

class AnthropicClient(BaseLLMClient):
    """Claude-3 Opus 클라이언트"""
    
    def __init__(self, api_key: str):
        if not anthropic:
            raise ImportError("anthropic package not installed")
        
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = "claude-3-opus-20240229"
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        Claude-3 Opus로 텍스트 생성
        
        Args:
            prompt: 사용자 프롬프트
            system_prompt: 시스템 프롬프트
            temperature: 생성 온도
            max_tokens: 최대 토큰 수
        
        Returns:
            생성된 텍스트
        """
        try:
            # Rate limiting for Claude API
            from app.core.rate_limiter import claude_rate_limiter
            estimated_tokens = len(prompt) // 4 + max_tokens
            await claude_rate_limiter.acquire(estimated_tokens)
            
            messages = [{"role": "user", "content": prompt}]
            
            response = await self.client.messages.create(
                model=self.model,
                messages=messages,
                system=system_prompt if system_prompt else "",
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            self.logger.info(f"Claude-3 Opus generated {len(response.content[0].text)} chars")
            return response.content[0].text
            
        except Exception as e:
            self.logger.error(f"Claude-3 Opus generation failed: {e}")
            raise
    
    def count_tokens(self, text: str) -> int:
        """
        토큰 수 추정 (Claude는 공식 토크나이저가 없으므로 추정)
        
        Args:
            text: 토큰을 계산할 텍스트
        
        Returns:
            추정 토큰 수
        """
        # Claude는 대략 4자당 1토큰으로 추정
        return len(text) // 4

class OpenAIClient(BaseLLMClient):
    """GPT-4 Turbo 클라이언트"""
    
    def __init__(self, api_key: str, model: Optional[str] = None):
        if not openai:
            raise ImportError("openai package not installed")
        
        self.client = openai.AsyncOpenAI(api_key=api_key)
        # Prefer provided model; fallback to a stable model id
        self.model = model or "gpt-4-0613"
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # 토크나이저 초기화
        try:
            self.tokenizer = tiktoken.encoding_for_model("gpt-4")
        except:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        GPT-4 Turbo로 텍스트 생성
        
        Args:
            prompt: 사용자 프롬프트
            system_prompt: 시스템 프롬프트
            temperature: 생성 온도
            max_tokens: 최대 토큰 수
        
        Returns:
            생성된 텍스트
        """
        try:
            # Rate limiting for OpenAI API
            from app.core.rate_limiter import openai_rate_limiter
            estimated_tokens = self.count_tokens(prompt) + max_tokens
            await openai_rate_limiter.acquire(estimated_tokens)
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            content = response.choices[0].message.content
            self.logger.info(f"GPT-4 Turbo generated {len(content)} chars, used {response.usage.total_tokens} tokens")
            return content
            
        except Exception as e:
            self.logger.error(f"GPT-4 Turbo generation failed: {e}")
            raise
    
    def count_tokens(self, text: str) -> int:
        """
        정확한 토큰 수 계산
        
        Args:
            text: 토큰을 계산할 텍스트
        
        Returns:
            토큰 수
        """
        return len(self.tokenizer.encode(text))

class LLMClient:
    """통합 LLM 클라이언트"""
    
    def __init__(self, model: str = "gpt-4-turbo"):
        """
        LLM 클라이언트 초기화
        
        Args:
            model: 사용할 모델 (gpt-4-turbo, claude-3-opus)
        """
        self.model = model
        self.client = None
        self.cache_enabled = True
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # 모델별 클라이언트 초기화
        if "claude" in model.lower():
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY not configured")
            self.client = AnthropicClient(settings.ANTHROPIC_API_KEY)
        else:  # Default to GPT-4
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not configured")
            self.client = OpenAIClient(settings.OPENAI_API_KEY, model=model)
    
    def _generate_cache_key(self, prompt: str, system_prompt: Optional[str], **kwargs) -> str:
        """
        캐시 키 생성
        
        Args:
            prompt: 프롬프트
            system_prompt: 시스템 프롬프트
            kwargs: 추가 파라미터
        
        Returns:
            캐시 키
        """
        cache_data = {
            "model": self.model,
            "prompt": prompt,
            "system_prompt": system_prompt,
            **kwargs
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return f"llm:{hashlib.md5(cache_str.encode()).hexdigest()}"
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        use_cache: bool = True,
        cache_ttl: int = 3600,
        **kwargs
    ) -> str:
        """
        LLM으로 텍스트 생성 (캐싱 포함)
        
        Args:
            prompt: 사용자 프롬프트
            system_prompt: 시스템 프롬프트
            temperature: 생성 온도
            max_tokens: 최대 토큰 수
            use_cache: 캐시 사용 여부
            cache_ttl: 캐시 TTL (초)
        
        Returns:
            생성된 텍스트
        """
        # 캐시 확인
        if use_cache and self.cache_enabled:
            cache_key = self._generate_cache_key(prompt, system_prompt, temperature=temperature)
            
            try:
                redis = await get_redis()
                cached_response = await redis.get(cache_key)
                if cached_response:
                    self.logger.info(f"Cache hit for prompt (key: {cache_key[:8]}...)")
                    return cached_response
            except Exception as e:
                self.logger.warning(f"Cache retrieval failed: {e}")
        
        # LLM 호출
        start_time = datetime.now()
        response = await self.client.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        generation_time = (datetime.now() - start_time).total_seconds()
        
        self.logger.info(f"Generated response in {generation_time:.2f}s")
        
        # 캐싱
        if use_cache and self.cache_enabled and response:
            try:
                redis = await get_redis()
                await redis.set(cache_key, response, cache_ttl)
                self.logger.info(f"Cached response (key: {cache_key[:8]}..., ttl: {cache_ttl}s)")
            except Exception as e:
                self.logger.warning(f"Cache storage failed: {e}")
        
        return response
    
    async def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        구조화된 응답 생성 (JSON)
        
        Args:
            prompt: 프롬프트
            system_prompt: 시스템 프롬프트
            response_format: 예상 응답 형식
        
        Returns:
            구조화된 응답 (딕셔너리)
        """
        # JSON 응답 요청 추가
        json_prompt = prompt + "\n\nPlease respond in valid JSON format."
        if response_format:
            json_prompt += f"\nExpected format: {json.dumps(response_format, indent=2)}"
        
        response = await self.generate(
            prompt=json_prompt,
            system_prompt=system_prompt,
            **kwargs
        )
        
        # JSON 파싱 시도
        try:
            # JSON 블록 추출 (```json ... ``` 형태 처리)
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            self.logger.debug(f"Raw response: {response}")
            # 폴백: 기본 구조 반환
            return {"error": "JSON parsing failed", "raw_response": response}
    
    def count_tokens(self, text: str) -> int:
        """
        토큰 수 계산
        
        Args:
            text: 텍스트
        
        Returns:
            토큰 수
        """
        return self.client.count_tokens(text)
    
    async def batch_generate(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> List[str]:
        """
        배치 생성 (병렬 처리)
        
        Args:
            prompts: 프롬프트 리스트
            system_prompt: 시스템 프롬프트
        
        Returns:
            생성된 텍스트 리스트
        """
        import asyncio
        
        tasks = [
            self.generate(prompt, system_prompt, **kwargs)
            for prompt in prompts
        ]
        
        return await asyncio.gather(*tasks)

# 싱글톤 인스턴스 생성 함수
def get_llm_client(model: str = "gpt-4-0613") -> LLMClient:
    """
    LLM 클라이언트 인스턴스 반환
    
    Args:
        model: 사용할 모델
    
    Returns:
        LLMClient 인스턴스
    """
    return LLMClient(model)
