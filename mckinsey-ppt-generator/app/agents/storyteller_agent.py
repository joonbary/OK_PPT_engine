"""
스토리텔링 에이전트
SCR 구조를 적용하여 설득력 있는 내러티브를 구성합니다.
"""

from typing import Dict, List
from app.agents.base_agent_v2 import BaseAgentV2
from app.db.models import AgentType
import json
from loguru import logger


class StorytellerAgent(BaseAgentV2):
    """
    McKinsey 커뮤니케이션 전문가
    
    역할:
    - SCR (Situation-Complication-Resolution) 구조 적용
    - 슬라이드 간 전환 문구 생성
    - 내러티브 일관성 유지
    - 발표자 노트 생성
    """
    
    def __init__(self):
        super().__init__(
            name="Storyteller Agent",
            agent_type=AgentType.STORYTELLER,
            model="gpt-4-turbo"
        )
        self.metrics = {}

    async def process(self, input_data: Dict, context: Dict) -> Dict:
        """
        스토리텔링 파이프라인
        
        Args:
            input_data: {
                'outline': List[Dict],  # StrategistAgent 출력
                'pyramid': Dict,        # StrategistAgent 출력
                'insights': List[Dict]  # DataAnalystAgent 출력
            }
            context: {
                'job_id': str
            }
        
        Returns:
            {
                'scr_structure': Dict,     # SCR 구조
                'transitions': List[str],  # 전환 문구
                'speaker_notes': List[str] # 발표자 노트
            }
        """
        logger.info(f"Starting storyteller processing for job {context.get('job_id')}")
        
        outline = input_data.get('outline', [])
        pyramid = input_data.get('pyramid', {})
        
        if not outline:
            raise ValueError("No outline provided to StorytellerAgent")
        
        import asyncio
        max_retries = 3
        
        # Step 1: SCR 구조 적용 (재시도 메커니즘)
        logger.info("Step 1: Applying SCR structure")
        scr_structure = None
        for attempt in range(max_retries):
            try:
                scr_structure = await asyncio.wait_for(
                    self._apply_scr_structure(outline, pyramid),
                    timeout=15.0  # 타임아웃 증가
                )
                logger.info(f"SCR structure applied successfully")
                break
            except asyncio.TimeoutError:
                logger.warning(f"SCR structure attempt {attempt+1} timed out")
                if attempt == max_retries - 1:
                    # 마지막 시도에서만 간단한 LLM 호출로 재시도
                    scr_structure = await self._apply_scr_structure_simple(outline)
            except Exception as e:
                logger.error(f"SCR structure attempt {attempt+1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
        
        # Step 2: 전환 문구 생성 (병렬 처리로 개선)
        logger.info("Step 2: Generating transitions")
        transitions = await self._generate_transitions_optimized(outline)
        
        # Step 3: 발표자 노트 생성 (병렬 처리로 개선)
        logger.info("Step 3: Creating speaker notes")
        speaker_notes = await self._create_speaker_notes_optimized(outline)
        
        self.metrics['slides_processed'] = len(outline)
        self.metrics['transitions_created'] = len(transitions)
        
        logger.info(f"Storyteller processing completed successfully")
        
        return {
            'scr_structure': scr_structure,
            'transitions': transitions,
            'speaker_notes': speaker_notes
        }
    
    async def _apply_scr_structure_simple(self, outline: List[Dict]) -> Dict:
        """
        간소화된 SCR 구조 적용 (재시도용)
        """
        total_slides = len(outline)
        
        # 슬라이드 수에 따른 자동 분배
        if total_slides <= 10:
            situation_end = 2
            complication_end = 4
        elif total_slides <= 15:
            situation_end = 3
            complication_end = 5
        else:
            situation_end = 4
            complication_end = 7
        
        return {
            'situation_slides': list(range(1, situation_end + 1)),
            'complication_slides': list(range(situation_end + 1, complication_end + 1)),
            'resolution_slides': list(range(complication_end + 1, total_slides - 1)),
            'story_arc': 'Current Situation Analysis -> Core Problem Definition -> Strategic Solutions -> Implementation Plan'
        }
    
    async def _apply_scr_structure(self, outline: List[Dict], pyramid: Dict) -> Dict:
        """
        SCR (Situation-Complication-Resolution) 구조 적용
        
        구조:
        - Situation: 현재 상황 (2-3장)
        - Complication: 문제/도전 (2-3장)
        - Resolution: 해결책 (나머지 대부분)
        
        Returns:
            {
                'situation_slides': List[int],
                'complication_slides': List[int],
                'resolution_slides': List[int],
                'story_arc': str
            }
        """
        prompt = f"""다음 슬라이드 아웃라인을 SCR 구조로 분류하세요.

슬라이드 수: {len(outline)}개
핵심 메시지: {pyramid.get('top_message', 'N/A')}

슬라이드 목록:
{json.dumps([{'number': s['slide_number'], 'title': s['title'], 'type': s.get('slide_type')} for s in outline], ensure_ascii=False, indent=2)}

다음 JSON 형식으로 반환:
{{
  "situation_slides": [슬라이드 번호 배열],
  "complication_slides": [슬라이드 번호 배열],
  "resolution_slides": [슬라이드 번호 배열],
  "story_arc": "스토리 전개 요약 (3-4문장)"
}}

분류 기준:
- Situation: 배경, 현황, 시장 분석 (2-3장)
- Complication: 문제점, 도전과제, 갭 분석 (2-3장)
- Resolution: 해결책, 전략, 실행 계획, 권고사항 (나머지)

JSON만 반환하세요."""

        response = await self.llm_client.generate(prompt)
        
        try:
            # response가 이미 dict일 수 있음
            if isinstance(response, dict):
                return response
            
            # JSON 블록 처리
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            
            scr = json.loads(response)
            return scr
        except (json.JSONDecodeError, TypeError):
            # 폴백: 기본 분류
            total = len(outline)
            return {
                'situation_slides': list(range(1, min(4, total))),
                'complication_slides': list(range(4, min(7, total))),
                'resolution_slides': list(range(7, total + 1)),
                'story_arc': 'Situation Analysis -> Problem Definition -> Solution Presentation'
            }
    
    async def _generate_transitions_optimized(self, outline: List[Dict]) -> List[str]:
        """
        최적화된 전환 문구 생성 (배치 처리)
        """
        if not outline:
            return []
        
        # Generate first transition using AI
        first_transition_prompt = f"Generate a professional opening statement for a business presentation titled '{outline[0].get('title', 'Business Presentation')}'. Return only the opening sentence."
        try:
            first_transition = await self.llm_client.generate(first_transition_prompt, max_tokens=50)
            transitions = [first_transition.strip()]
        except Exception as e:
            logger.error(f"Failed to generate opening transition: {e}")
            raise RuntimeError("Cannot generate opening transition: AI generation required")
        
        # 나머지 슬라이드들에 대한 전환 문구를 한 번의 LLM 호출로 생성
        if len(outline) > 1:
            slide_pairs = []
            for i in range(1, len(outline)):
                slide_pairs.append({
                    'prev': outline[i-1].get('title', ''),
                    'prev_type': outline[i-1].get('slide_type', ''),
                    'curr': outline[i].get('title', ''),
                    'curr_type': outline[i].get('slide_type', '')
                })
            
            prompt = f"""다음 슬라이드 쌍들에 대한 자연스러운 전환 문구를 생성하세요.
각 전환은 한 문장으로, JSON 배열로 반환하세요.

슬라이드 정보:
{json.dumps(slide_pairs, ensure_ascii=False, indent=2)}

각 슬라이드 타입별 전환 가이드:
- situation: 현재 상황을 설명하는 도입
- complication: 문제점이나 과제로의 전환
- resolution: 해결책 제시로의 전환
- recommendation: 최종 권고사항으로의 전환

JSON 배열 형식으로 반환: ["전환1", "전환2", ...]"""
            
            try:
                response = await self.llm_client.generate(prompt, max_tokens=1000)
                
                # JSON 파싱
                if "```json" in response:
                    json_start = response.find("```json") + 7
                    json_end = response.find("```", json_start)
                    response = response[json_start:json_end].strip()
                
                generated_transitions = json.loads(response)
                
                if isinstance(generated_transitions, list):
                    # 생성된 전환 문구 사용
                    if len(generated_transitions) >= len(slide_pairs):
                        transitions.extend(generated_transitions[:len(slide_pairs)])
                    else:
                        # 개수가 부족한 경우 개별 생성으로 재시도
                        logger.warning(f"Generated {len(generated_transitions)} transitions, expected {len(slide_pairs)}. Retrying individually...")
                        
                        # 생성된 것은 사용
                        transitions.extend(generated_transitions)
                        
                        # 부족한 부분만 개별 생성
                        for i in range(len(generated_transitions), len(slide_pairs)):
                            pair = slide_pairs[i]
                            retry_prompt = f"""Generate a natural transition sentence from "{pair['prev']}" to "{pair['curr']}".
                            Return only the transition sentence, no quotes or JSON."""
                            
                            try:
                                single_transition = await self.llm_client.generate(retry_prompt, max_tokens=100)
                                transitions.append(single_transition.strip())
                            except Exception as retry_e:
                                logger.error(f"Failed to generate individual transition: {retry_e}")
                                raise RuntimeError(f"Cannot generate transition for slide {i+2}: AI generation required")
                else:
                    raise ValueError(f"Invalid response format: expected list, got {type(generated_transitions)}")
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse transition JSON: {e}")
                raise RuntimeError(f"Transition generation failed - AI response parsing error: {e}")
            except Exception as e:
                logger.error(f"Batch transition generation failed: {e}")
                raise RuntimeError(f"Transition generation failed: {e}")
        
        return transitions
    
    # Fallback methods removed - AI only
    
    async def _generate_transitions(self, outline: List[Dict]) -> List[str]:
        """기존 메서드 - 호환성 유지"""
        return await self._generate_transitions_optimized(outline)
    
    async def _create_speaker_notes_optimized(self, outline: List[Dict]) -> List[str]:
        """
        최적화된 발표자 노트 생성
        """
        if not outline:
            return []
        
        # 배치로 LLM 호출하여 발표자 노트 생성
        slides_info = []
        for slide in outline:
            slides_info.append({
                'number': slide.get('slide_number', 0),
                'title': slide.get('title', ''),
                'type': slide.get('slide_type', ''),
                'headline': slide.get('headline', ''),
                'key_points': slide.get('key_points', [])
            })
        
        prompt = f"""다음 슬라이드들에 대한 발표자 노트를 생성하세요.
각 노트는 발표자가 참고할 핵심 내용을 포함해야 합니다.

슬라이드 정보:
{json.dumps(slides_info, ensure_ascii=False, indent=2)}

각 슬라이드별로 다음을 포함한 JSON 배열 반환:
[
  {{
    "slide_number": 1,
    "speaking_points": ["포인트1", "포인트2"],
    "emphasis": "강조할 핵심",
    "potential_questions": ["예상 질문1", "예상 질문2"]
  }},
  ...
]"""
        
        try:
            response = await self.llm_client.generate(prompt, max_tokens=2000)
            
            # JSON 파싱
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            
            # JSON 파싱 전에 일반적인 문제 수정
            # 이스케이프되지 않은 따옴표 처리
            import re
            # 줄바꿈 문자를 공백으로 변경
            response = response.replace('\n\n', ' ').replace('\n', ' ')
            # 제어 문자 제거
            response = ''.join(char for char in response if ord(char) >= 32 or char == '\n')
            
            try:
                notes_data = json.loads(response)
            except json.JSONDecodeError as je:
                logger.warning(f"JSON parsing failed, attempting to fix: {je}")
                # 여러 수정 방법 시도
                try:
                    # 방법 1: 이스케이프되지 않은 따옴표 처리
                    fixed_response = re.sub(r'(?<!\\)"(?![:,\]\}\s])', r'\"', response)
                    notes_data = json.loads(fixed_response)
                except:
                    try:
                        # 방법 2: 개별 객체들을 배열로 감싸기
                        if not response.strip().startswith('['):
                            wrapped_response = '[' + response + ']'
                            notes_data = json.loads(wrapped_response)
                        else:
                            # 방법 3: 각 슬라이드에 대해 기본값 생성
                            logger.warning("All JSON parsing attempts failed, generating default notes")
                            notes_data = []
                            for i, slide in enumerate(outline):
                                notes_data.append({
                                    "slide_number": slide.get('slide_number', i+1),
                                    "speaking_points": [f"Present {slide.get('title', 'content')} clearly", "Emphasize key data points"],
                                    "emphasis": slide.get('headline', 'Key message'),
                                    "potential_questions": ["What are the implications?", "How does this compare to alternatives?"]
                                })
                    except:
                        # 최종 폴백
                        notes_data = []
            
            # 포맷팅
            notes = []
            for i, slide in enumerate(outline):
                if i < len(notes_data):
                    note_info = notes_data[i]
                    speaking_points = '\n'.join(f"- {p}" for p in note_info.get('speaking_points', []))
                    questions = '\n'.join(f"- {q}" for q in note_info.get('potential_questions', []))
                    
                    note = f"""[슬라이드 {slide['slide_number']}] {slide['title']}

핵심 메시지:
{slide.get('headline', note_info.get('emphasis', ''))}

발표 포인트:
{speaking_points}

Emphasis:
{note_info.get('emphasis', '')}

예상 질문:
{questions}"""
                else:
                    # 데이터가 부족한 경우 AI로 개별 생성
                    note = await self._create_default_speaker_note_ai(slide)
                
                notes.append(note)
            
            return notes
            
        except Exception as e:
            logger.error(f"Failed to create speaker notes: {e}")
            raise RuntimeError(f"Speaker notes generation failed - AI generation required: {e}")
    
    async def _create_default_speaker_note_ai(self, slide: Dict) -> str:
        """AI를 사용한 개별 발표자 노트 생성"""
        prompt = f"""Generate professional speaker notes for this presentation slide:
        
Slide #{slide.get('slide_number', 0)}: {slide.get('title', '')}
Type: {slide.get('slide_type', '')}
Headline: {slide.get('headline', '')}
Key Points: {', '.join(slide.get('key_points', []))}

Return structured speaker notes including:
1. Key message to emphasize
2. Main talking points
3. Supporting data to mention
4. Transition to next slide

Keep it concise but comprehensive."""
        
        try:
            response = await self.llm_client.generate(prompt, max_tokens=300)
            return f"[Slide {slide.get('slide_number', 0)}] {slide.get('title', '')}\n\n{response.strip()}"
        except Exception as e:
            logger.error(f"Failed to generate AI speaker note: {e}")
            raise RuntimeError(f"Cannot generate speaker note for slide {slide.get('slide_number', 0)}: AI generation required")
    
    async def _create_speaker_notes(self, outline: List[Dict]) -> List[str]:
        """기존 메서드 - 호환성 유지"""
        return await self._create_speaker_notes_optimized(outline)
