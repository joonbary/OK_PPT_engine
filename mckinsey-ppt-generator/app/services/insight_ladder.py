"""
McKinsey 4단계 Insight Ladder
Level 1: Observation (관찰) - "매출 10% 증가"
Level 2: Comparison (비교) - "경쟁사 대비 2배"
Level 3: Implication (원인/상관) - "신제품이 70% 기여"
Level 4: Action (전략/권고) - "라인 확대로 20% 추가 성장 가능"
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re
import logging

logger = logging.getLogger(__name__)


class InsightLevel(Enum):
    """인사이트 수준"""
    OBSERVATION = 1      # "매출 10% 증가"
    COMPARISON = 2       # "경쟁사 대비 2배"
    IMPLICATION = 3      # "신제품이 원인"
    ACTION = 4          # "라인 확대 필요"


@dataclass
class Insight:
    """인사이트 데이터"""
    level: InsightLevel
    statement: str
    evidence: List[str]
    confidence: float
    metrics: Optional[Dict] = None


class InsightLadder:
    """
    데이터를 4단계 인사이트로 변환
    
    McKinsey 방식:
    1. 데이터 관찰 → 2. 비교 분석 → 3. 원인 파악 → 4. 전략 제시
    """
    
    # 비교 키워드
    COMPARISON_KEYWORDS = [
        "대비", "비교", "차이", "배", "배수", "초과", "미만",
        "높은", "낮은", "빠른", "느린", "많은", "적은"
    ]
    
    # 원인 키워드
    IMPLICATION_KEYWORDS = [
        "원인", "기여", "영향", "결과", "효과", "때문", "덕분",
        "요인", "이유", "배경", "근거", "상관"
    ]
    
    # 전략 키워드
    ACTION_KEYWORDS = [
        "전략", "필요", "권고", "제안", "실행", "추진", "가능",
        "확대", "강화", "개선", "투자", "집중", "전환"
    ]
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def climb(self, data: Dict) -> List[Insight]:
        """
        데이터에서 4단계 인사이트 생성
        
        Args:
            data: 원본 데이터 {
                "metric": "매출",
                "value": 1000,
                "previous_value": 900,
                "benchmark": 950,
                "period": "2024년",
                "drivers": {"신제품": 70, "기존제품": 30}
            }
        
        Returns:
            List[Insight]: Level 1-4 인사이트 리스트
        """
        insights = []
        
        try:
            # Level 1: Observation
            observation = self._create_observation(data)
            insights.append(observation)
            
            # Level 2: Comparison
            comparison = self._create_comparison(data, observation)
            insights.append(comparison)
            
            # Level 3: Implication
            implication = self._create_implication(data, comparison)
            insights.append(implication)
            
            # Level 4: Action
            action = self._create_action(data, implication)
            insights.append(action)
            
            self.logger.info(f"Generated {len(insights)} level insights")
            return insights
            
        except Exception as e:
            self.logger.error(f"Insight generation failed: {e}")
            # 폴백: Level 1만 반환
            return [self._create_fallback_observation(data)]
    
    def _create_observation(self, data: Dict) -> Insight:
        """
        Level 1: 단순 관찰
        예: "2024년 매출이 1000억원이다"
        """
        metric = data.get("metric", "값")
        value = data.get("value", 0)
        period = data.get("period", "현재")
        unit = data.get("unit", "")
        
        # 숫자 포맷팅
        formatted_value = self._format_number(value, unit)
        
        statement = f"{period} {metric}이 {formatted_value}"
        
        return Insight(
            level=InsightLevel.OBSERVATION,
            statement=statement,
            evidence=[f"데이터: {metric}={value}"],
            confidence=1.0,
            metrics={"value": value}
        )
    
    def _create_comparison(self, data: Dict, observation: Insight) -> Insight:
        """
        Level 2: 비교 분석
        예: "전년 대비 10% 증가, 경쟁사 5% 대비 2배 빠름"
        """
        current = data.get("value", 0)
        previous = data.get("previous_value")
        benchmark = data.get("benchmark")
        metric = data.get("metric", "값")
        
        comparisons = []
        metrics = {"value": current}
        
        # 1. 전년 대비 비교
        if previous is not None and previous > 0:
            growth_rate = ((current - previous) / previous) * 100
            metrics["growth_rate"] = growth_rate
            
            if growth_rate > 0:
                comparisons.append(f"전년 대비 {abs(growth_rate):.1f}% 증가")
            elif growth_rate < 0:
                comparisons.append(f"전년 대비 {abs(growth_rate):.1f}% 감소")
            else:
                comparisons.append("전년과 동일")
        
        # 2. 벤치마크 대비 비교
        if benchmark is not None and benchmark > 0:
            vs_benchmark = current / benchmark
            metrics["vs_benchmark"] = vs_benchmark
            
            if vs_benchmark > 1.2:
                comparisons.append(f"업계 평균 대비 {vs_benchmark:.1f}배 높음")
            elif vs_benchmark < 0.8:
                comparisons.append(f"업계 평균 대비 {(1-vs_benchmark)*100:.1f}% 낮음")
            else:
                comparisons.append("업계 평균 수준")
        
        # 비교 문구 결합
        if comparisons:
            statement = ", ".join(comparisons)
        else:
            # 폴백: 절대값 강조
            formatted_value = self._format_number(current, data.get("unit", ""))
            statement = f"{metric} {formatted_value}로 높은 수준"
        
        return Insight(
            level=InsightLevel.COMPARISON,
            statement=statement,
            evidence=[observation.statement],
            confidence=0.9 if comparisons else 0.6,
            metrics=metrics
        )
    
    def _create_implication(self, data: Dict, comparison: Insight) -> Insight:
        """
        Level 3: 원인/상관관계
        예: "신제품 출시가 매출 성장의 70% 기여"
        """
        drivers = data.get("drivers", {})
        metric = data.get("metric", "변화")
        
        if drivers:
            # 가장 큰 기여 요인 찾기
            main_driver = max(drivers.items(), key=lambda x: x[1])
            driver_name, contribution = main_driver
            
            statement = f"{driver_name}이 {metric}의 {contribution:.0f}% 기여"
            confidence = 0.85
            evidence = [comparison.statement, f"기여도 분석: {drivers}"]
            
        else:
            # 폴백: 비교 결과에서 추론
            if "증가" in comparison.statement:
                statement = "시장 확대 및 제품 경쟁력 강화가 주요 원인"
                confidence = 0.7
            elif "감소" in comparison.statement:
                statement = "시장 환경 악화 또는 경쟁 심화가 주요 원인"
                confidence = 0.7
            else:
                statement = "복합적 요인에 의한 결과로 추정"
                confidence = 0.6
            
            evidence = [comparison.statement]
        
        return Insight(
            level=InsightLevel.IMPLICATION,
            statement=statement,
            evidence=evidence,
            confidence=confidence,
            metrics=comparison.metrics
        )
    
    def _create_action(self, data: Dict, implication: Insight) -> Insight:
        """
        Level 4: 전략적 권고
        예: "신제품 라인 3개로 확대하여 20% 추가 성장 가능"
        """
        metric = data.get("metric", "성과")
        current = data.get("value", 0)
        
        # 전략 매핑
        action_statement = self._generate_action_recommendation(
            implication.statement,
            metric,
            current,
            data
        )
        
        return Insight(
            level=InsightLevel.ACTION,
            statement=action_statement,
            evidence=[implication.statement],
            confidence=0.75,
            metrics=implication.metrics
        )
    
    def _generate_action_recommendation(
        self,
        implication: str,
        metric: str,
        current_value: float,
        data: Dict
    ) -> str:
        """
        함의에서 실행 가능한 권고사항 도출
        
        매핑 로직:
        - "기여" → 해당 영역 투자 확대
        - "증가" → 모멘텀 유지 전략
        - "감소" → 개선 조치
        - "경쟁" → 차별화 전략
        """
        implication_lower = implication.lower()
        
        # 1. 기여 요인 기반 전략
        if "기여" in implication_lower:
            # 주요 기여자 추출
            match = re.search(r'(\w+)이', implication)
            if match:
                driver = match.group(1)
                return f"{driver} 영역 투자 확대로 {metric} 30% 추가 성장 가능"
            else:
                return f"핵심 성장 동력 강화로 {metric} 지속 성장 가능"
        
        # 2. 증가 트렌드 기반 전략
        elif "증가" in implication_lower or "성장" in implication_lower:
            return f"성장 모멘텀 유지 위한 선제적 투자로 {metric} 극대화 필요"
        
        # 3. 감소 트렌드 기반 전략
        elif "감소" in implication_lower or "악화" in implication_lower:
            return f"{metric} 개선 위한 즉각적 대응 조치 및 구조 개선 필요"
        
        # 4. 경쟁 관련 전략
        elif "경쟁" in implication_lower:
            return f"경쟁 우위 확보 위한 차별화 전략 수립 및 실행 필요"
        
        # 5. 시장 관련 전략
        elif "시장" in implication_lower:
            return f"시장 변화 대응 전략 마련 및 신속한 실행 필요"
        
        # 6. 기본 전략
        else:
            return f"{metric} 최적화 위한 전략적 접근 및 투자 필요"
    
    def _format_number(self, value: float, unit: str = "") -> str:
        """숫자 포맷팅 (한국식)"""
        if value >= 10000:
            # 억 단위
            eok = value / 10000
            if eok >= 10000:
                # 조 단위
                jo = eok / 10000
                return f"{jo:.1f}조{unit}"
            return f"{eok:.1f}억{unit}"
        elif value >= 1000:
            return f"{value:,.0f}{unit}"
        else:
            return f"{value:.1f}{unit}"
    
    def _create_fallback_observation(self, data: Dict) -> Insight:
        """
        폴백 관찰 (데이터 없을 때)
        """
        return Insight(
            level=InsightLevel.OBSERVATION,
            statement="데이터 분석 중",
            evidence=["원본 데이터 부족"],
            confidence=0.3,
            metrics={}
        )


class InsightEnhancer:
    """기존 콘텐츠를 4단계 인사이트로 강화"""
    
    def __init__(self):
        """초기화"""
        self.ladder = InsightLadder()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def enhance_slide(self, slide_content: Dict) -> Dict:
        """
        슬라이드 콘텐츠를 4단계 인사이트로 강화
        
        Before:
        - 제목: "매출 현황"
        - 내용: "2024년 매출 1000억"
        
        After:
        - 제목: "신제품 출시로 매출 20% 급증, 추가 투자 필요"
        - 내용: 
            - Level 2: "전년 대비 20% 증가, 업계 평균 대비 2배"
            - Level 3: "신제품이 70% 기여"
            - Level 4: "신제품 라인 확대로 30% 추가 성장 가능"
        
        Args:
            slide_content: 원본 슬라이드 콘텐츠
        
        Returns:
            Dict: 강화된 슬라이드 콘텐츠
        """
        try:
            # 데이터 추출
            data = self._extract_data_from_content(slide_content)
            
            # 인사이트 생성
            insights = self.ladder.climb(data)
            
            # Level 4 (Action)를 제목으로 사용
            enhanced_title = insights[3].statement if len(insights) >= 4 else slide_content.get("title", "제목 없음")
            
            # Level 2-4를 본문으로 사용
            enhanced_content = []
            if len(insights) >= 4:
                enhanced_content = [
                    f"• {insights[1].statement}",  # Level 2: Comparison
                    f"• {insights[2].statement}",  # Level 3: Implication
                    f"• {insights[3].statement}"   # Level 4: Action
                ]
            else:
                # 폴백: 원본 콘텐츠 유지
                enhanced_content = slide_content.get("content", [])
            
            # 결과 반환
            result = {
                **slide_content,
                "title": enhanced_title,
                "content": enhanced_content,
                "insights": [i.statement for i in insights],
                "insight_level": insights[-1].level.value if insights else 1,
                "confidence": insights[-1].confidence if insights else 0.5
            }
            
            self.logger.info(f"Enhanced slide to Level {result['insight_level']}")
            return result
            
        except Exception as e:
            self.logger.error(f"Slide enhancement failed: {e}")
            # 폴백: 원본 반환
            return slide_content
    
    def _extract_data_from_content(self, content: Dict) -> Dict:
        """
        슬라이드 콘텐츠에서 데이터 추출
        
        추출 항목:
        - metric: 지표명
        - value: 현재값
        - previous_value: 이전값
        - benchmark: 벤치마크
        - period: 기간
        - drivers: 기여 요인
        """
        data = {}
        
        # 1. 명시적 데이터 필드
        if "data" in content:
            data.update(content["data"])
        
        # 2. 제목에서 추출
        title = content.get("title", "")
        data["metric"] = self._extract_metric_from_text(title)
        
        # 3. 본문에서 숫자 추출
        body = content.get("body", "")
        if isinstance(body, list):
            body = " ".join(body)
        
        numbers = self._extract_numbers_from_text(body)
        if numbers:
            data["value"] = numbers[0]
            if len(numbers) > 1:
                data["previous_value"] = numbers[1]
        
        # 4. 기본값 설정
        data.setdefault("metric", "지표")
        data.setdefault("value", 100)
        data.setdefault("period", "현재")
        data.setdefault("unit", "")
        
        return data
    
    def _extract_metric_from_text(self, text: str) -> str:
        """텍스트에서 지표명 추출"""
        # 일반적인 지표 키워드
        metrics = [
            "매출", "수익", "이익", "비용", "시장", "점유율",
            "성장률", "만족도", "효율", "생산성", "품질"
        ]
        
        for metric in metrics:
            if metric in text:
                return metric
        
        # 폴백: 첫 단어
        words = text.split()
        return words[0] if words else "지표"
    
    def _extract_numbers_from_text(self, text: str) -> List[float]:
        """
        텍스트에서 숫자 추출"""
        # 숫자 패턴 (퍼센트, 배수, 억 등 포함)
        patterns = [
            r'(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*배',
            r'(\d+\.?\d*)\s*억',
            r'(\d+\.?\d*)\s*조',
            r'(\d+\.?\d*)'
        ]
        
        numbers = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    numbers.append(float(match))
                except ValueError:
                    continue
        
        return numbers


class InsightQualityEvaluator:
    """인사이트 품질 평가"""
    
    def evaluate(self, insights: List[Insight]) -> Dict[str, any]:
        """
        인사이트 리스트 품질 평가
        
        평가 기준:
        1. 레벨 도달도 (최고 레벨)
        2. 신뢰도 평균
        3. 증거 충분성
        4. 정량화 포함
        
        Returns:
            {
                "score": float (0-1),
                "max_level": int (1-4),
                "avg_confidence": float,
                "has_quantification": bool,
                "quality_grade": str ("A"/"B"/"C"/"D")
            }
        """
        if not insights:
            return {
                "score": 0.0,
                "max_level": 0,
                "avg_confidence": 0.0,
                "has_quantification": False,
                "quality_grade": "F"
            }
        
        # 1. 최고 레벨
        max_level = max(i.level.value for i in insights)
        
        # 2. 평균 신뢰도
        avg_confidence = sum(i.confidence for i in insights) / len(insights)
        
        # 3. 정량화 포함 여부
        has_quantification = any(
            re.search(r'\d+', i.statement) for i in insights
        )
        
        # 4. 종합 점수 계산
        score = (
            (max_level / 4.0) * 0.4 +      # 레벨 (40%)
            avg_confidence * 0.3 +          # 신뢰도 (30%)
            (1.0 if has_quantification else 0.5) * 0.3  # 정량화 (30%)
        )
        
        # 5. 등급 결정
        if score >= 0.9:
            grade = "A"
        elif score >= 0.8:
            grade = "B"
        elif score >= 0.7:
            grade = "C"
        elif score >= 0.6:
            grade = "D"
        else:
            grade = "F"
        
        return {
            "score": score,
            "max_level": max_level,
            "avg_confidence": avg_confidence,
            "has_quantification": has_quantification,
            "quality_grade": grade
        }
