"""
McKinsey 수준의 액션 지향적 헤드라인 생성
- So What 테스트 자동 적용
- SCQA 구조 (Situation-Complication-Question-Answer)
- 정량화 강제
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class HeadlineTemplate:
    """헤드라인 템플릿"""
    pattern: str
    example: str
    score_weight: float
    category: str  # 'growth', 'comparison', 'strategic', 'financial'


class HeadlineGenerator:
    """
    McKinsey 표준 헤드라인 생성기
    
    핵심 원칙:
    1. 액션 지향적 (동사 포함)
    2. 정량화 (숫자 포함)
    3. So What 통과 (전략적 함의)
    4. 한 문장으로 핵심 전달
    """
    
    # McKinsey 헤드라인 패턴 (4가지)
    TEMPLATES = [
        HeadlineTemplate(
            pattern="{주체}가 {기간} 내 {수치}% {동사}하여 {결과}",
            example="아시아 시장이 3년 내 50% 성장하여 최대 기회 제공",
            score_weight=1.0,
            category="growth"
        ),
        HeadlineTemplate(
            pattern="{비교대상} 대비 {수치}배 {형용사}한 {주체}가 {결과}",
            example="경쟁사 대비 2배 빠른 성장률이 시장 리더십 확보",
            score_weight=0.95,
            category="comparison"
        ),
        HeadlineTemplate(
            pattern="{주체}의 {특성}이 {수치}% 개선으로 {목표} 달성 가능",
            example="제품 품질 20% 개선으로 프리미엄 시장 진입 가능",
            score_weight=0.90,
            category="strategic"
        ),
        HeadlineTemplate(
            pattern="{전략}을 통해 {기간} 내 {수치}{단위} {목표} 실현",
            example="디지털 전환으로 2년 내 1000억원 비용 절감 실현",
            score_weight=0.85,
            category="financial"
        )
    ]
    
    # McKinsey 키워드
    ACTION_VERBS = [
        "제공", "확보", "달성", "실현", "개선", "증가", "감소", 
        "전환", "확대", "강화", "구축", "창출", "도출"
    ]
    
    IMPLICATION_KEYWORDS = [
        "가능", "필요", "실현", "확보", "달성", "기회", "위협", 
        "중요", "핵심", "우선", "주요", "전략적"
    ]
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def generate(
        self, 
        content: Dict, 
        slide_type: str = "content"
    ) -> str:
        """
        콘텐츠에서 McKinsey 수준 헤드라인 생성
        
        Args:
            content: 슬라이드 콘텐츠 (title, body, data 포함)
            slide_type: 슬라이드 유형 (title/content/conclusion)
        
        Returns:
            str: 액션 지향적 헤드라인
        """
        try:
            # 1. 기존 제목 추출
            original_title = content.get("title", "")
            
            # 2. 키워드 추출
            keywords = self._extract_keywords(content)
            
            # 3. 숫자 추출
            numbers = self._extract_numbers(content)
            
            # 4. 템플릿 선택
            template = self._select_template(slide_type, keywords, numbers)
            
            # 5. 헤드라인 생성
            headline = self._fill_template(template, keywords, numbers, content)
            
            # 6. So What 테스트
            if not self._passes_so_what_test(headline):
                headline = self._enhance_with_implication(headline, content)
            
            # 7. 최종 검증
            headline = self._finalize_headline(headline, original_title)
            
            self.logger.info(f"Generated headline: {headline}")
            return headline
            
        except Exception as e:
            self.logger.error(f"Headline generation failed: {e}")
            # 폴백: 원본 제목 개선
            return self._improve_existing_title(content.get("title", "제목 없음"))
    
    def _extract_keywords(self, content: Dict) -> List[str]:
        """
        콘텐츠에서 핵심 키워드 추출
        
        우선순위:
        1. 명사 (주체, 대상)
        2. 동사 (액션)
        3. 형용사 (특성)
        """
        keywords = []
        
        # 제목에서 추출
        title = content.get("title", "")
        keywords.extend(self._tokenize(title))
        
        # 본문에서 추출
        body = content.get("body", "")
        if isinstance(body, list):
            body = " ".join(body)
        keywords.extend(self._tokenize(body))
        
        # 중복 제거 및 상위 5개 반환
        unique_keywords = list(dict.fromkeys(keywords))
        return unique_keywords[:5]
    
    def _tokenize(self, text: str) -> List[str]:
        """간단한 토큰화 (공백 기준)"""
        if not text:
            return []
        
        # 특수문자 제거
        text = re.sub(r'[^\w\s%]', '', text)
        
        # 공백으로 분리
        tokens = text.split()
        
        # 2글자 이상만 반환
        return [t for t in tokens if len(t) >= 2]
    
    def _extract_numbers(self, content: Dict) -> List[float]:
        """
        콘텐츠에서 숫자 추출
        """
        numbers = []
        
        # 전체 콘텐츠 문자열화
        text = str(content)
        
        # 숫자 패턴 매칭
        # 예: 10%, 1000억, 2.5배, 50명
        patterns = [
            r'(\d+\.?\d*)\s*%',      # 퍼센트
            r'(\d+\.?\d*)\s*배',      # 배수
            r'(\d+\.?\d*)\s*억',      # 억 단위
            r'(\d+\.?\d*)\s*만',      # 만 단위
            r'(\d+\.?\d*)',           # 일반 숫자
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            numbers.extend([float(m) for m in matches if m])
        
        return numbers[:3]  # 상위 3개
    
    def _select_template(
        self, 
        slide_type: str, 
        keywords: List[str], 
        numbers: List[float]
    ) -> HeadlineTemplate:
        """
        슬라이드 타입과 콘텐츠에 맞는 템플릿 선택
        
        선택 로직:
        1. 숫자 많음 + 비교 키워드 → comparison
        2. 성장/증가 키워드 → growth
        3. 전략/목표 키워드 → strategic
        4. 금액/비용 키워드 → financial
        """
        # 키워드 기반 카테고리 감지
        keyword_str = " ".join(keywords).lower()
        
        if any(word in keyword_str for word in ["대비", "비교", "경쟁"]):
            category = "comparison"
        elif any(word in keyword_str for word in ["성장", "증가", "확대"]):
            category = "growth"
        elif any(word in keyword_str for word in ["억", "원", "비용", "매출"]):
            category = "financial"
        else:
            category = "strategic"
        
        # 카테고리에 맞는 템플릿 찾기
        for template in self.TEMPLATES:
            if template.category == category:
                return template
        
        # 기본값: 첫 번째 템플릿
        return self.TEMPLATES[0]
    
    def _fill_template(
        self, 
        template: HeadlineTemplate, 
        keywords: List[str], 
        numbers: List[float],
        content: Dict
    ) -> str:
        """
        템플릿에 실제 값 채우기
        
        예시:
        템플릿: "{주체}가 {기간} 내 {수치}% {동사}하여 {결과}"
        입력: keywords=["시장", "성장"], numbers=[50]
        출력: "시장이 3년 내 50% 성장하여 최대 기회 제공"
        """
        # 기본값 설정
        subject = keywords[0] if keywords else "주요 영역"
        action = self._select_action_verb(keywords)
        number = int(numbers[0]) if numbers else 10
        result = self._generate_result(keywords, number)
        
        # 템플릿 카테고리별 처리
        if template.category == "growth":
            return f"{subject}이 3년 내 {number}% {action}하여 {result}"
        
        elif template.category == "comparison":
            benchmark = keywords[1] if len(keywords) > 1 else "업계 평균"
            multiplier = round(number / 10) if number > 10 else 2
            return f"{benchmark} 대비 {multiplier}배 빠른 {subject}이 {result}"
        
        elif template.category == "strategic":
            characteristic = keywords[1] if len(keywords) > 1 else "핵심 역량"
            return f"{subject}의 {characteristic}이 {number}% 개선으로 {result}"
        
        elif template.category == "financial":
            amount_str = f"{number}억원" if number < 1000 else f"{int(number/1000)}조원"
            return f"{subject}의 {action}을 통해 2년 내 {amount_str} {result}"
        
        # 폴백
        return f"{subject}이 {number}% {action}하여 {result}"
    
    def _select_action_verb(self, keywords: List[str]) -> str:
        """키워드에서 적절한 액션 동사 선택"""
        keyword_str = " ".join(keywords).lower()
        
        verb_map = {
            "성장": "성장",
            "증가": "증가",
            "개선": "개선",
            "확대": "확대",
            "강화": "강화",
            "감소": "절감",
        }
        
        for keyword, verb in verb_map.items():
            if keyword in keyword_str:
                return verb
        
        return "개선"  # 기본값
    
    def _generate_result(self, keywords: List[str], number: float) -> str:
        """결과 문구 생성"""
        keyword_str = " ".join(keywords).lower()
        
        # 긍정적 결과
        if number > 0:
            if "시장" in keyword_str:
                return "시장 선점 기회 확보"
            elif "경쟁" in keyword_str:
                return "경쟁 우위 강화 가능"
            elif "비용" in keyword_str:
                return "비용 절감 실현"
            elif "매출" in keyword_str:
                return "매출 성장 가속화"
            else:
                return "목표 달성 가능"
        
        # 부정적 결과 (음수)
        else:
            return "개선 조치 필요"
    
    def _passes_so_what_test(self, headline: str) -> bool:
        """
        So What 테스트
        
        통과 기준:
        1. 동사 포함 (액션)
        2. 숫자 포함 (정량화)
        3. 함의 키워드 ("가능", "필요" 등)
        4. 20자 이상 (충분한 정보)
        """
        has_verb = any(verb in headline for verb in self.ACTION_VERBS)
        has_number = bool(re.search(r'\d+', headline))
        has_implication = any(word in headline for word in self.IMPLICATION_KEYWORDS)
        sufficient_length = len(headline) >= 20
        
        return all([has_verb, has_number, has_implication, sufficient_length])
    
    def _enhance_with_implication(self, headline: str, content: Dict) -> str:
        """
        전략적 함의 추가
        
        변환 예시:
        "시장이 성장한다" 
        → "시장 성장으로 조기 진입 시 선점 효과 확보 가능"
        """
        implication_patterns = {
            "성장": "선점 효과 확보 가능",
            "증가": "경쟁 우위 강화 기회",
            "감소": "비용 절감 실현 가능",
            "개선": "목표 달성 가능",
            "변화": "시장 재편 주도 필요",
            "차이": "차별화 전략 수립 필요",
        }
        
        for keyword, implication in implication_patterns.items():
            if keyword in headline:
                # 이미 함의 포함 시 중복 방지
                if any(imp in headline for imp in self.IMPLICATION_KEYWORDS):
                    return headline
                return f"{headline}, {implication}"
        
        # 기본 함의 추가
        if not any(imp in headline for imp in self.IMPLICATION_KEYWORDS):
            return f"{headline}, 전략적 대응 필요"
        
        return headline
    
    def _finalize_headline(self, headline: str, original: str) -> str:
        """
        최종 헤드라인 검증 및 조정
        
        - 최대 길이 제한 (60자)
        - 최소 길이 보장 (20자)
        - 마침표 제거
        """
        # 마침표 제거
        headline = headline.rstrip(".")
        
        # 길이 검증
        if len(headline) > 60:
            # 60자로 자르고 "..." 추가
            headline = headline[:57] + "..."
        
        elif len(headline) < 20:
            # 원본 제목 활용하여 보강
            if original and len(original) > 5:
                headline = f"{original} - {headline}"
        
        return headline
    
    def _improve_existing_title(self, title: str) -> str:
        """
        기존 제목 개선 (폴백)
        
        예시:
        "시장 분석" → "시장 분석을 통한 전략적 방향 제시"
        """
        if not title or len(title) < 3:
            return "핵심 인사이트 및 전략적 시사점"
        
        # 이미 좋은 제목이면 그대로
        if len(title) >= 20 and any(verb in title for verb in self.ACTION_VERBS):
            return title
        
        # 개선 패턴
        improvements = [
            f"{title}을 통한 핵심 인사이트 도출",
            f"{title} 분석 및 전략적 시사점",
            f"{title} 현황과 향후 방향성",
        ]
        
        # 길이에 맞는 개선안 선택
        for improved in improvements:
            if 20 <= len(improved) <= 60:
                return improved
        
        return improvements[0]


class SoWhatTester:
    """
    So What 테스트 자동화
    """
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def test(self, headline: str) -> Dict[str, any]:
        """
        McKinsey So What 테스트
        
        Returns:
            {
                "passed": bool,
                "score": float (0-1),
                "issues": List[str],
                "suggestions": List[str]
            }
        """
        issues = []
        suggestions = []
        score = 1.0
        
        # 1. 액션성 검사 (30%)
        if not self._has_action_verb(headline):
            issues.append("액션 동사 부재")
            suggestions.append("'제공', '확보', '달성', '실현' 등 동사 추가")
            score -= 0.3
        
        # 2. 정량화 검사 (30%)
        if not self._has_quantification(headline):
            issues.append("정량화 부재")
            suggestions.append("구체적 숫자나 비율 추가 (예: 20%, 2배)")
            score -= 0.3
        
        # 3. 함의 검사 (20%)
        if not self._has_implication(headline):
            issues.append("전략적 함의 부재")
            suggestions.append("'가능', '필요', '확보' 등 함의 키워드 추가")
            score -= 0.2
        
        # 4. 길이 검사 (20%)
        if len(headline) < 20:
            issues.append("헤드라인 너무 짧음 (20자 미만)")
            suggestions.append("배경이나 결과 추가하여 20자 이상 작성")
            score -= 0.2
        elif len(headline) > 60:
            issues.append("헤드라인 너무 김 (60자 초과)")
            suggestions.append("핵심만 남기고 60자 이내로 축약")
            score -= 0.1
        
        result = {
            "passed": score >= 0.7,
            "score": max(0.0, score),
            "issues": issues,
            "suggestions": suggestions
        }
        
        self.logger.info(f"So What test result: {result}")
        return result
    
    def _has_action_verb(self, headline: str) -> bool:
        """액션 동사 포함 여부"""
        action_verbs = [
            "제공", "확보", "달성", "실현", "개선", "증가", "감소",
            "전환", "확대", "강화", "구축", "창출", "도출", "가능", "필요"
        ]
        return any(verb in headline for verb in action_verbs)
    
    def _has_quantification(self, headline: str) -> bool:
        """정량화 포함 여부"""
        # 숫자 패턴
        return bool(re.search(r'\d+', headline))
    
    def _has_implication(self, headline: str) -> bool:
        """함의 키워드 포함 여부"""
        implication_keywords = [
            "가능", "필요", "실현", "확보", "달성", "기회", "위협",
            "중요", "핵심", "우선", "주요", "전략적"
        ]
        return any(keyword in headline for keyword in implication_keywords)
