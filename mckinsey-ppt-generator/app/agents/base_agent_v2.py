"""
강화된 BaseAgent 클래스
LLM 통합, 시스템 프롬프트 관리, 성능 메트릭 포함
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
import logging
import json
import os
from datetime import datetime
from app.core.llm_client import get_llm_client, LLMClient
from app.db.models import AgentType, AgentLog
from app.core.config import settings

class BaseAgentV2(ABC):
    """
    에이전트 베이스 클래스 (강화 버전)
    모든 특화 에이전트의 기반 클래스
    """
    
    def __init__(
        self,
        name: str,
        agent_type: AgentType,
        model: str = "gpt-4-turbo",
        temperature: float = 0.7
    ):
        """
        에이전트 초기화
        
        Args:
            name: 에이전트 이름
            agent_type: 에이전트 타입
            model: 사용할 LLM 모델
            temperature: 생성 온도
        """
        self.name = name
        self.agent_type = agent_type
        self.model = model
        self.temperature = temperature
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # LLM 클라이언트 초기화
        self.llm_client: LLMClient = get_llm_client(model)
        
        # 시스템 프롬프트 로드
        self.system_prompt = self._load_system_prompt()
        
        # 성능 메트릭
        self.total_tokens_used = 0
        self.total_execution_time = 0.0
        self.execution_count = 0
    
    def _load_system_prompt(self) -> str:
        """
        시스템 프롬프트 파일 로드
        
        Returns:
            시스템 프롬프트 텍스트
        """
        prompt_file = f"app/prompts/{self.agent_type.value}_prompt.txt"
        
        # 프롬프트 파일이 존재하면 로드
        if os.path.exists(prompt_file):
            try:
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except Exception as e:
                self.logger.warning(f"Failed to load prompt file: {e}")
        
        # 기본 프롬프트 반환
        return self._get_default_prompt()
    
    def _get_default_prompt(self) -> str:
        """
        기본 시스템 프롬프트 반환
        
        Returns:
            에이전트 타입별 기본 프롬프트
        """
        prompts = {
            AgentType.STRATEGIST: """You are a strategic consultant specializing in McKinsey-style presentations.
            Focus on high-level insights, strategic implications, and executive-level recommendations.
            Analyze business situations comprehensively and provide actionable strategic guidance.""",
            
            AgentType.ANALYST: """You are a data analyst expert specializing in McKinsey-style analysis.
            Extract key insights from data, perform quantitative analysis, and present findings clearly.
            Focus on data-driven insights, comparisons, benchmarks, and trend analysis.""",
            
            AgentType.STORYTELLER: """You are a narrative expert specializing in business storytelling.
            Create compelling storylines that connect data points into coherent business narratives.
            Use the pyramid principle and MECE structure to organize content logically.""",
            
            AgentType.DESIGNER: """You are a presentation design specialist focusing on McKinsey standards.
            Ensure visual hierarchy, clarity, and professional aesthetics.
            Apply McKinsey design principles: simplicity, consistency, and impact.""",
            
            AgentType.REVIEWER: """You are a quality assurance expert for McKinsey-level presentations.
            Review presentations for clarity, accuracy, and adherence to McKinsey standards.
            Ensure all content passes the So What test and provides actionable insights."""
        }
        return prompts.get(self.agent_type, "You are a professional consultant creating McKinsey-style presentations.")
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        입력 데이터 처리 (서브클래스에서 구현)
        
        Args:
            input_data: 처리할 입력 데이터
        
        Returns:
            처리 결과
        """
        pass
    
    async def _generate_content(
        self,
        prompt: str,
        use_system_prompt: bool = True,
        **kwargs
    ) -> str:
        """
        LLM을 사용하여 콘텐츠 생성
        
        Args:
            prompt: 사용자 프롬프트
            use_system_prompt: 시스템 프롬프트 사용 여부
            kwargs: 추가 생성 파라미터
        
        Returns:
            생성된 텍스트
        """
        try:
            start_time = datetime.now()
            
            # 시스템 프롬프트 설정
            system_prompt = self.system_prompt if use_system_prompt else None
            
            # LLM 호출
            response = await self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=self.temperature,
                **kwargs
            )
            
            # 메트릭 업데이트
            execution_time = (datetime.now() - start_time).total_seconds()
            self.total_execution_time += execution_time
            self.execution_count += 1
            
            # 토큰 수 계산
            tokens_used = self.llm_client.count_tokens(prompt + response)
            self.total_tokens_used += tokens_used
            
            self.logger.info(
                f"Generated content: {len(response)} chars, "
                f"{tokens_used} tokens, {execution_time:.2f}s"
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Content generation failed: {e}")
            raise
    
    async def _generate_structured(
        self,
        prompt: str,
        response_format: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        구조화된 응답 생성
        
        Args:
            prompt: 프롬프트
            response_format: 예상 응답 형식
        
        Returns:
            구조화된 응답
        """
        try:
            response = await self.llm_client.generate_structured(
                prompt=prompt,
                system_prompt=self.system_prompt,
                response_format=response_format,
                temperature=self.temperature,
                **kwargs
            )
            return response
        except Exception as e:
            self.logger.error(f"Structured generation failed: {e}")
            raise
    
    def create_log_entry(
        self,
        job_id: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        prompt: str,
        response: str,
        execution_time: float,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> AgentLog:
        """
        에이전트 로그 엔트리 생성
        
        Args:
            job_id: 작업 ID
            input_data: 입력 데이터
            output_data: 출력 데이터
            prompt: 사용된 프롬프트
            response: LLM 응답
            execution_time: 실행 시간
            success: 성공 여부
            error_message: 에러 메시지
        
        Returns:
            AgentLog 엔트리
        """
        return AgentLog(
            job_id=job_id,
            agent_type=self.agent_type,
            agent_name=self.name,
            input_data=input_data,
            output_data=output_data,
            prompt=prompt[:5000],  # 길이 제한
            response=response[:5000],  # 길이 제한
            execution_time_seconds=execution_time,
            tokens_used=self.llm_client.count_tokens(prompt + response),
            model_used=self.model,
            success=success,
            error_message=error_message
        )
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        에이전트 성능 메트릭 반환
        
        Returns:
            성능 메트릭 딕셔너리
        """
        avg_execution_time = (
            self.total_execution_time / self.execution_count
            if self.execution_count > 0 else 0
        )
        
        return {
            "agent_name": self.name,
            "agent_type": self.agent_type.value,
            "model": self.model,
            "total_tokens_used": self.total_tokens_used,
            "total_execution_time": self.total_execution_time,
            "execution_count": self.execution_count,
            "average_execution_time": avg_execution_time
        }
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        입력 데이터 유효성 검증
        
        Args:
            input_data: 검증할 입력 데이터
        
        Returns:
            유효성 여부
        """
        # 기본 검증 (서브클래스에서 확장 가능)
        if not input_data:
            self.logger.error("Input data is empty")
            return False
        return True
    
    async def batch_process(
        self,
        input_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        배치 처리
        
        Args:
            input_list: 입력 데이터 리스트
        
        Returns:
            처리 결과 리스트
        """
        results = []
        for input_data in input_list:
            try:
                result = await self.process(input_data)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Batch processing error: {e}")
                results.append({"error": str(e), "input": input_data})
        return results