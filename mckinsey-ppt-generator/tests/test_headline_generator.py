"""
HeadlineGenerator 단위 테스트
- McKinsey 수준 헤드라인 생성
- So What 테스트
- ContentGenerator 통합
"""

import unittest
from unittest.mock import Mock, patch
import logging

from app.services.headline_generator import HeadlineGenerator, SoWhatTester, HeadlineTemplate
from app.models.workflow_models import SlideGenerationSpec

# 로깅 설정
logging.basicConfig(level=logging.INFO)


class TestHeadlineGenerator(unittest.TestCase):
    """HeadlineGenerator 테스트"""
    
    def setUp(self):
        """테스트 초기화"""
        self.generator = HeadlineGenerator()
        
    def test_headline_generation_basic(self):
        """기본 헤드라인 생성 테스트"""
        content = {
            "title": "시장 분석",
            "body": "아시아 시장이 50% 성장했다",
            "data": {"growth": 50}
        }
        
        headline = self.generator.generate(content)
        
        # 헤드라인이 생성되었는지
        self.assertIsNotNone(headline)
        self.assertIsInstance(headline, str)
        
        # 최소 길이 충족
        self.assertGreaterEqual(len(headline), 20)
        
        # 최대 길이 제한
        self.assertLessEqual(len(headline), 60)
        
    def test_headline_with_numbers(self):
        """숫자 포함 헤드라인 생성 테스트"""
        content = {
            "title": "매출 성장",
            "body": "매출이 작년 대비 35% 증가, 1000억원 달성",
            "data": {"revenue": 1000, "growth": 35}
        }
        
        headline = self.generator.generate(content)
        
        # 숫자가 포함되어 있는지
        import re
        self.assertTrue(bool(re.search(r'\d+', headline)))
        
    def test_action_verb_inclusion(self):
        """액션 동사 포함 테스트"""
        content = {
            "title": "전략 실행",
            "body": "디지털 전환을 통해 비용 절감 실현"
        }
        
        headline = self.generator.generate(content)
        
        # 액션 동사 포함 확인
        action_verbs = self.generator.ACTION_VERBS
        has_verb = any(verb in headline for verb in action_verbs)
        self.assertTrue(has_verb)
        
    def test_different_slide_types(self):
        """다양한 슬라이드 타입 테스트"""
        test_cases = [
            ("title", "프레젠테이션 제목"),
            ("content", "분석 내용"),
            ("conclusion", "결론 및 제언")
        ]
        
        for slide_type, title in test_cases:
            content = {"title": title, "body": "내용"}
            headline = self.generator.generate(content, slide_type=slide_type)
            
            # 각 타입별로 헤드라인이 생성되는지
            self.assertIsNotNone(headline)
            
    def test_keyword_extraction(self):
        """키워드 추출 테스트"""
        content = {
            "title": "디지털 혁신 전략",
            "body": "클라우드 도입으로 효율성 증대 및 비용 절감"
        }
        
        keywords = self.generator._extract_keywords(content)
        
        # 키워드가 추출되었는지
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)
        self.assertLessEqual(len(keywords), 5)
        
    def test_number_extraction(self):
        """숫자 추출 테스트"""
        content = {
            "title": "실적 보고",
            "body": "매출 1500억원, 성장률 25%, 시장점유율 3.5배 증가"
        }
        
        numbers = self.generator._extract_numbers(content)
        
        # 숫자가 추출되었는지
        self.assertIsInstance(numbers, list)
        self.assertGreater(len(numbers), 0)
        self.assertLessEqual(len(numbers), 3)
        
    def test_template_selection(self):
        """템플릿 선택 로직 테스트"""
        # 성장 카테고리
        growth_keywords = ["시장", "성장", "확대"]
        template = self.generator._select_template("content", growth_keywords, [50])
        self.assertEqual(template.category, "growth")
        
        # 비교 카테고리
        comparison_keywords = ["경쟁사", "대비", "비교"]
        template = self.generator._select_template("content", comparison_keywords, [200])
        self.assertEqual(template.category, "comparison")
        
        # 재무 카테고리
        financial_keywords = ["매출", "억원", "비용"]
        template = self.generator._select_template("content", financial_keywords, [1000])
        self.assertEqual(template.category, "financial")
        
    def test_so_what_test_pass(self):
        """So What 테스트 통과 케이스"""
        # 좋은 헤드라인 (동사, 숫자, 함의, 충분한 길이)
        good_headline = "아시아 시장이 3년 내 50% 성장하여 시장 선점 기회 확보 가능"
        
        result = self.generator._passes_so_what_test(good_headline)
        self.assertTrue(result)
        
    def test_so_what_test_fail(self):
        """So What 테스트 실패 케이스"""
        # 나쁜 헤드라인들
        bad_headlines = [
            "시장 분석",  # 너무 짧고 동사/숫자/함의 없음
            "시장이 성장하고 있다",  # 숫자와 함의 없음
            "50% 증가",  # 동사와 함의 없음, 너무 짧음
        ]
        
        for headline in bad_headlines:
            result = self.generator._passes_so_what_test(headline)
            self.assertFalse(result)
            
    def test_implication_enhancement(self):
        """전략적 함의 추가 테스트"""
        headline_without_implication = "시장이 30% 성장"
        
        enhanced = self.generator._enhance_with_implication(
            headline_without_implication, 
            {}
        )
        
        # 함의가 추가되었는지
        self.assertIn("가능", enhanced)
        self.assertGreater(len(enhanced), len(headline_without_implication))
        
    def test_headline_finalization(self):
        """헤드라인 최종 처리 테스트"""
        # 너무 긴 헤드라인
        long_headline = "아" * 70
        finalized = self.generator._finalize_headline(long_headline, "")
        self.assertLessEqual(len(finalized), 60)
        self.assertTrue(finalized.endswith("..."))
        
        # 너무 짧은 헤드라인
        short_headline = "분석"
        original = "시장 분석 보고서"
        finalized = self.generator._finalize_headline(short_headline, original)
        self.assertGreaterEqual(len(finalized), 20)
        
    def test_fallback_improvement(self):
        """폴백 제목 개선 테스트"""
        # 빈 제목
        improved = self.generator._improve_existing_title("")
        self.assertEqual(improved, "핵심 인사이트 및 전략적 시사점")
        
        # 짧은 제목
        improved = self.generator._improve_existing_title("분석")
        self.assertIn("분석", improved)
        self.assertGreaterEqual(len(improved), 20)
        
        # 이미 좋은 제목
        good_title = "디지털 전환을 통한 비용 30% 절감 실현 가능"
        improved = self.generator._improve_existing_title(good_title)
        self.assertEqual(improved, good_title)


class TestSoWhatTester(unittest.TestCase):
    """SoWhatTester 테스트"""
    
    def setUp(self):
        """테스트 초기화"""
        self.tester = SoWhatTester()
        
    def test_perfect_headline(self):
        """완벽한 헤드라인 테스트"""
        perfect_headline = "매출 50% 증가로 시장 리더십 확보 가능"
        
        result = self.tester.test(perfect_headline)
        
        self.assertTrue(result["passed"])
        self.assertEqual(result["score"], 1.0)
        self.assertEqual(len(result["issues"]), 0)
        self.assertEqual(len(result["suggestions"]), 0)
        
    def test_missing_action_verb(self):
        """액션 동사 누락 테스트"""
        headline = "시장 점유율 30% 상황에서 전략 필요"
        
        result = self.tester.test(headline)
        
        self.assertLess(result["score"], 1.0)
        self.assertIn("액션 동사 부재", result["issues"])
        self.assertGreater(len(result["suggestions"]), 0)
        
    def test_missing_quantification(self):
        """정량화 누락 테스트"""
        headline = "시장 성장을 통해 경쟁 우위 확보 가능"
        
        result = self.tester.test(headline)
        
        self.assertLess(result["score"], 1.0)
        self.assertIn("정량화 부재", result["issues"])
        
    def test_missing_implication(self):
        """함의 누락 테스트"""
        headline = "매출이 50% 증가하여 성장"
        
        result = self.tester.test(headline)
        
        self.assertLess(result["score"], 1.0)
        self.assertIn("전략적 함의 부재", result["issues"])
        
    def test_too_short_headline(self):
        """너무 짧은 헤드라인 테스트"""
        headline = "매출 50% 증가"
        
        result = self.tester.test(headline)
        
        self.assertLess(result["score"], 1.0)
        self.assertIn("너무 짧음", " ".join(result["issues"]))
        
    def test_too_long_headline(self):
        """너무 긴 헤드라인 테스트"""
        headline = "매출이 50% 증가하여 " + "추가 내용 " * 20 + "달성 가능"
        
        result = self.tester.test(headline)
        
        self.assertLess(result["score"], 1.0)
        self.assertIn("너무 김", " ".join(result["issues"]))


class TestContentGeneratorIntegration(unittest.TestCase):
    """ContentGenerator 통합 테스트"""
    
    def setUp(self):
        """테스트 초기화"""
        from app.services.content_generator import ContentGenerator
        self.content_generator = ContentGenerator()
        
    def test_headline_generator_integration(self):
        """HeadlineGenerator 통합 확인"""
        # HeadlineGenerator가 초기화되었는지
        self.assertTrue(hasattr(self.content_generator, 'headline_generator'))
        self.assertIsInstance(self.content_generator.headline_generator, HeadlineGenerator)
        
    def test_mckinsey_headline_generation(self):
        """McKinsey 헤드라인 생성 메서드 테스트"""
        spec = SlideGenerationSpec(
            slide_number=2,
            title="비용 절감 전략",
            content_type="content",
            content={
                "bullets": [
                    "운영 비용 30% 절감 목표",
                    "자동화를 통한 효율성 개선",
                    "2년 내 ROI 달성"
                ]
            },
            layout_type="title_and_content"
        )
        
        headline = self.content_generator._generate_mckinsey_headline(spec)
        
        # 헤드라인이 개선되었는지
        self.assertIsNotNone(headline)
        self.assertNotEqual(headline, spec.title)  # 원본과 다름
        self.assertGreaterEqual(len(headline), 20)  # 충분한 길이
        
    def test_body_extraction_from_spec(self):
        """SlideGenerationSpec에서 본문 추출 테스트"""
        # 불릿 포인트가 있는 경우
        spec_with_bullets = SlideGenerationSpec(
            slide_number=1,
            title="Test",
            content_type="content",
            content={"bullets": ["Point 1", "Point 2", "Point 3"]}
        )
        
        body = self.content_generator._extract_body_from_spec(spec_with_bullets)
        self.assertIn("Point 1", body)
        self.assertIn("Point 2", body)
        
        # 차트 인사이트가 있는 경우
        spec_with_insights = SlideGenerationSpec(
            slide_number=2,
            title="Chart",
            content_type="chart",
            content={"insights": ["Insight 1", "Insight 2"]}
        )
        
        body = self.content_generator._extract_body_from_spec(spec_with_insights)
        self.assertIn("Insight 1", body)
        
        # 비교 콘텐츠가 있는 경우
        spec_with_comparison = SlideGenerationSpec(
            slide_number=3,
            title="Comparison",
            content_type="comparison",
            content={
                "option_a": {"points": ["A1", "A2"]},
                "option_b": {"points": ["B1", "B2"]}
            }
        )
        
        body = self.content_generator._extract_body_from_spec(spec_with_comparison)
        self.assertIn("A1", body)
        self.assertIn("B1", body)
        
    def test_fallback_on_error(self):
        """오류 시 폴백 테스트"""
        spec = SlideGenerationSpec(
            slide_number=1,
            title="원본 제목",
            content_type="content",
            content=None  # None으로 오류 유발
        )
        
        # 오류가 발생해도 원본 제목이 반환되어야 함
        headline = self.content_generator._generate_mckinsey_headline(spec)
        self.assertEqual(headline, "원본 제목")


if __name__ == "__main__":
    unittest.main()