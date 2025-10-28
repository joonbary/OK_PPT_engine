"""
InsightLadder 단위 테스트 (15개 케이스)
- McKinsey 4단계 인사이트 생성
- ContentGenerator 통합
"""

import unittest
from unittest.mock import Mock, patch
import logging

from app.services.insight_ladder import (
    InsightLadder, InsightEnhancer, InsightQualityEvaluator,
    InsightLevel, Insight
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)


class TestInsightLadder(unittest.TestCase):
    """InsightLadder 테스트 (7개)"""
    
    def setUp(self):
        """테스트 초기화"""
        self.ladder = InsightLadder()
        
    def test_1_complete_insight_generation(self):
        """완전한 4단계 인사이트 생성 테스트"""
        data = {
            "metric": "매출",
            "value": 1000,
            "previous_value": 900,
            "benchmark": 950,
            "period": "2024년",
            "unit": "억원",
            "drivers": {"신제품": 70, "기존제품": 30}
        }
        
        insights = self.ladder.climb(data)
        
        # 4개 레벨 모두 생성되었는지
        self.assertEqual(len(insights), 4)
        
        # 각 레벨이 올바른지
        self.assertEqual(insights[0].level, InsightLevel.OBSERVATION)
        self.assertEqual(insights[1].level, InsightLevel.COMPARISON)
        self.assertEqual(insights[2].level, InsightLevel.IMPLICATION)
        self.assertEqual(insights[3].level, InsightLevel.ACTION)
        
    def test_2_observation_level(self):
        """Level 1: 관찰 인사이트 테스트"""
        data = {
            "metric": "이익",
            "value": 500,
            "period": "2024년 Q1",
            "unit": "억원"
        }
        
        observation = self.ladder._create_observation(data)
        
        # 기본 관찰 문장 생성
        self.assertIn("2024년 Q1", observation.statement)
        self.assertIn("이익", observation.statement)
        self.assertIn("500", observation.statement)
        self.assertEqual(observation.level, InsightLevel.OBSERVATION)
        self.assertEqual(observation.confidence, 1.0)
        
    def test_3_comparison_with_growth(self):
        """Level 2: 성장 비교 인사이트 테스트"""
        data = {
            "metric": "매출",
            "value": 120,
            "previous_value": 100,
            "benchmark": 110
        }
        
        observation = self.ladder._create_observation(data)
        comparison = self.ladder._create_comparison(data, observation)
        
        # 성장률 계산 확인
        self.assertIn("20.0% 증가", comparison.statement)
        self.assertEqual(comparison.level, InsightLevel.COMPARISON)
        self.assertGreater(comparison.confidence, 0.8)
        
    def test_4_comparison_with_decline(self):
        """Level 2: 감소 비교 인사이트 테스트"""
        data = {
            "metric": "비용",
            "value": 80,
            "previous_value": 100
        }
        
        observation = self.ladder._create_observation(data)
        comparison = self.ladder._create_comparison(data, observation)
        
        # 감소율 계산 확인
        self.assertIn("20.0% 감소", comparison.statement)
        
    def test_5_implication_with_drivers(self):
        """Level 3: 기여도 분석 인사이트 테스트"""
        data = {
            "metric": "성장",
            "value": 150,
            "drivers": {"디지털": 60, "오프라인": 30, "기타": 10}
        }
        
        observation = self.ladder._create_observation(data)
        comparison = self.ladder._create_comparison(data, observation)
        implication = self.ladder._create_implication(data, comparison)
        
        # 최대 기여 요인 확인
        self.assertIn("디지털", implication.statement)
        self.assertIn("60%", implication.statement)
        self.assertEqual(implication.level, InsightLevel.IMPLICATION)
        
    def test_6_action_recommendation(self):
        """Level 4: 전략 권고 인사이트 테스트"""
        data = {
            "metric": "매출",
            "value": 200,
            "drivers": {"신규고객": 80, "기존고객": 20}
        }
        
        insights = self.ladder.climb(data)
        action = insights[-1]  # 마지막이 Action
        
        # 전략적 권고 포함
        self.assertEqual(action.level, InsightLevel.ACTION)
        self.assertIn("투자", action.statement)
        self.assertGreater(len(action.statement), 10)
        
    def test_7_number_formatting(self):
        """숫자 포맷팅 테스트"""
        # 억 단위
        self.assertEqual(self.ladder._format_number(10000, "원"), "1.0억원")
        
        # 조 단위
        self.assertEqual(self.ladder._format_number(100000000, "원"), "1.0조원")
        
        # 천 단위
        self.assertEqual(self.ladder._format_number(5000, "개"), "5,000개")
        
        # 소수점
        self.assertEqual(self.ladder._format_number(99.5, "%"), "99.5%")


class TestInsightEnhancer(unittest.TestCase):
    """InsightEnhancer 테스트 (5개)"""
    
    def setUp(self):
        """테스트 초기화"""
        self.enhancer = InsightEnhancer()
        
    def test_8_slide_enhancement_basic(self):
        """기본 슬라이드 강화 테스트"""
        slide_content = {
            "title": "매출 현황",
            "body": "2024년 매출 1000억원",
            "data": {
                "metric": "매출",
                "value": 1000,
                "previous_value": 800,
                "unit": "억원"
            }
        }
        
        enhanced = self.enhancer.enhance_slide(slide_content)
        
        # 강화된 제목과 콘텐츠
        self.assertNotEqual(enhanced["title"], slide_content["title"])
        self.assertIsInstance(enhanced["content"], list)
        self.assertGreater(len(enhanced["insights"]), 0)
        self.assertGreaterEqual(enhanced["insight_level"], 1)
        
    def test_9_data_extraction_from_text(self):
        """텍스트에서 데이터 추출 테스트"""
        content = {
            "title": "시장 점유율 분석",
            "body": "현재 점유율 35%, 작년 30%"
        }
        
        data = self.enhancer._extract_data_from_content(content)
        
        # 지표명 추출
        self.assertIn("시장", data["metric"])
        
        # 숫자 추출
        numbers = self.enhancer._extract_numbers_from_text(content["body"])
        self.assertIn(35.0, numbers)
        self.assertIn(30.0, numbers)
        
    def test_10_metric_extraction(self):
        """지표명 추출 테스트"""
        # 매출 추출
        self.assertEqual(
            self.enhancer._extract_metric_from_text("매출 성장 분석"),
            "매출"
        )
        
        # 이익 추출
        self.assertEqual(
            self.enhancer._extract_metric_from_text("영업이익 현황"),
            "이익"
        )
        
        # 폴백
        self.assertEqual(
            self.enhancer._extract_metric_from_text("기타 데이터"),
            "기타"
        )
        
    def test_11_number_extraction_patterns(self):
        """다양한 숫자 패턴 추출 테스트"""
        text = "매출 1500억원, 성장률 25%, 시장점유율 3.5배 증가, 직원 200명"
        
        numbers = self.enhancer._extract_numbers_from_text(text)
        
        # 다양한 패턴의 숫자들
        self.assertIn(1500.0, numbers)
        self.assertIn(25.0, numbers)
        self.assertIn(3.5, numbers)
        self.assertIn(200.0, numbers)
        
    def test_12_fallback_on_error(self):
        """오류 시 폴백 테스트"""
        # 빈 콘텐츠
        slide_content = {}
        
        enhanced = self.enhancer.enhance_slide(slide_content)
        
        # 원본 반환
        self.assertEqual(enhanced, slide_content)


class TestInsightQualityEvaluator(unittest.TestCase):
    """InsightQualityEvaluator 테스트 (3개)"""
    
    def setUp(self):
        """테스트 초기화"""
        self.evaluator = InsightQualityEvaluator()
        
    def test_13_perfect_insights(self):
        """완벽한 인사이트 평가 테스트"""
        insights = [
            Insight(InsightLevel.OBSERVATION, "매출 100억", ["data"], 1.0),
            Insight(InsightLevel.COMPARISON, "전년 대비 20% 증가", ["obs"], 0.9),
            Insight(InsightLevel.IMPLICATION, "신제품이 70% 기여", ["comp"], 0.85),
            Insight(InsightLevel.ACTION, "투자 확대로 30% 성장 가능", ["impl"], 0.8)
        ]
        
        result = self.evaluator.evaluate(insights)
        
        # 높은 점수와 A 등급
        self.assertGreater(result["score"], 0.8)
        self.assertEqual(result["max_level"], 4)
        self.assertTrue(result["has_quantification"])
        self.assertIn(result["quality_grade"], ["A", "B"])
        
    def test_14_partial_insights(self):
        """부분적 인사이트 평가 테스트"""
        insights = [
            Insight(InsightLevel.OBSERVATION, "현황 분석", ["data"], 0.7),
            Insight(InsightLevel.COMPARISON, "비교 결과", ["obs"], 0.6)
        ]
        
        result = self.evaluator.evaluate(insights)
        
        # 중간 점수
        self.assertEqual(result["max_level"], 2)
        self.assertLess(result["score"], 0.7)
        self.assertFalse(result["has_quantification"])
        self.assertIn(result["quality_grade"], ["C", "D", "F"])
        
    def test_15_empty_insights(self):
        """빈 인사이트 평가 테스트"""
        result = self.evaluator.evaluate([])
        
        # 최저 점수
        self.assertEqual(result["score"], 0.0)
        self.assertEqual(result["max_level"], 0)
        self.assertEqual(result["quality_grade"], "F")


if __name__ == "__main__":
    unittest.main()