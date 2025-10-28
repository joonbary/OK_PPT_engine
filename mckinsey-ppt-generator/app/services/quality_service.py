"""
Quality Service - Fix #4
품질 검증 및 자동 수정 서비스
"""

from typing import Dict, Any, List, Optional
from pptx import Presentation
import logging
from app.core.quality_validator import McKinseyQualityValidator

logger = logging.getLogger(__name__)


class QualityService:
    """품질 검증 및 자동 수정 서비스"""
    
    def __init__(self):
        self.validator = McKinseyQualityValidator()
        self.quality_threshold = 0.85
        self.max_iterations = 3
    
    async def validate_and_improve_presentation(
        self, 
        prs: Presentation, 
        auto_fix: bool = True,
        target_quality: float = None
    ) -> Dict[str, Any]:
        """
        프레젠테이션 품질 검증 및 개선
        
        Args:
            prs: PowerPoint 프레젠테이션
            auto_fix: 자동 수정 여부
            target_quality: 목표 품질 점수
            
        Returns:
            검증 및 개선 결과
        """
        if target_quality is None:
            target_quality = self.quality_threshold
        
        logger.info(f"🔍 품질 검증 시작 (목표: {target_quality:.2f})")
        
        all_results = []
        iteration = 0
        current_quality = 0.0
        
        while iteration < self.max_iterations:
            iteration += 1
            logger.info(f"📋 품질 검증 반복 {iteration}/{self.max_iterations}")
            
            # 품질 검증 및 자동 수정
            result = self.validator.validate_presentation(prs, auto_fix=auto_fix)
            current_quality = result['quality_score']
            
            all_results.append({
                'iteration': iteration,
                'quality_score': current_quality,
                'issues_found': result['total_issues'],
                'fixes_applied': result['total_fixes'],
                'passed': result['passed']
            })
            
            logger.info(f"반복 {iteration} 결과: 품질 {current_quality:.3f}, 이슈 {result['total_issues']}개, 수정 {result['total_fixes']}개")
            
            # 목표 품질에 도달하거나 더 이상 개선되지 않으면 중단
            if current_quality >= target_quality:
                logger.info(f"✅ 목표 품질 달성: {current_quality:.3f} >= {target_quality:.2f}")
                break
            
            if result['total_fixes'] == 0:
                logger.info("ℹ️ 더 이상 자동 수정할 내용이 없음")
                break
        
        # 최종 결과
        final_result = {
            'final_quality_score': current_quality,
            'target_quality': target_quality,
            'quality_achieved': current_quality >= target_quality,
            'total_iterations': iteration,
            'iteration_results': all_results,
            'total_issues_resolved': sum(r['fixes_applied'] for r in all_results),
            'improvement': all_results[-1]['quality_score'] - all_results[0]['quality_score'] if all_results else 0
        }
        
        # 최종 상세 검증
        final_validation = self.validator.validate_presentation(prs, auto_fix=False)
        final_result['final_validation'] = final_validation
        
        logger.info(f"🎯 최종 품질: {current_quality:.3f}, 개선도: {final_result['improvement']:.3f}")
        
        return final_result
    
    def generate_improvement_recommendations(self, validation_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """개선 권장사항 생성"""
        recommendations = []
        
        issues = validation_result.get('issues', {})
        
        # 스타일 위반 권장사항
        style_violations = issues.get('style_violations', [])
        if style_violations:
            font_issues = [v for v in style_violations if v['type'] == 'wrong_font']
            color_issues = [v for v in style_violations if v['type'] == 'wrong_color']
            
            if font_issues:
                recommendations.append({
                    'category': 'style',
                    'priority': 'high',
                    'title': '폰트 표준화',
                    'description': f'{len(font_issues)}개 슬라이드에서 비표준 폰트 사용됨',
                    'action': 'Arial 폰트로 통일',
                    'automated': True
                })
            
            if color_issues:
                recommendations.append({
                    'category': 'style',
                    'priority': 'medium',
                    'title': '색상 표준화',
                    'description': f'{len(color_issues)}개 요소에서 McKinsey 색상 가이드 위반',
                    'action': 'McKinsey 브랜드 색상으로 수정',
                    'automated': True
                })
        
        # 레이아웃 문제 권장사항
        layout_issues = issues.get('layout_issues', [])
        if layout_issues:
            missing_titles = [i for i in layout_issues if i['type'] == 'missing_title']
            
            if missing_titles:
                recommendations.append({
                    'category': 'layout',
                    'priority': 'high',
                    'title': '제목 추가',
                    'description': f'{len(missing_titles)}개 슬라이드에 제목 누락',
                    'action': '각 슬라이드에 명확한 제목 추가',
                    'automated': False
                })
        
        # 텍스트 문제 권장사항
        text_problems = issues.get('text_problems', [])
        if text_problems:
            overflow_issues = [p for p in text_problems if 'overflow' in p['type']]
            
            if overflow_issues:
                recommendations.append({
                    'category': 'layout',
                    'priority': 'high',
                    'title': '텍스트 오버플로우 수정',
                    'description': f'{len(overflow_issues)}개 요소에서 텍스트가 슬라이드 경계 초과',
                    'action': '텍스트 박스 크기 조정 또는 내용 단축',
                    'automated': True
                })
        
        # 차트 문제 권장사항
        chart_errors = issues.get('chart_errors', [])
        if chart_errors:
            small_charts = [e for e in chart_errors if e['type'] == 'chart_too_small']
            
            if small_charts:
                recommendations.append({
                    'category': 'visualization',
                    'priority': 'medium',
                    'title': '차트 크기 최적화',
                    'description': f'{len(small_charts)}개 차트가 너무 작음',
                    'action': '차트 크기를 가독성을 위해 확대',
                    'automated': True
                })
        
        # 우선순위별 정렬
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return recommendations
    
    def create_quality_dashboard(self, validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """품질 대시보드 데이터 생성"""
        if not validation_results:
            return {}
        
        latest = validation_results[-1]
        
        # 품질 트렌드
        quality_trend = [r['quality_score'] for r in validation_results]
        
        # 이슈 카테고리별 분포
        issues = latest.get('final_validation', {}).get('issues', {})
        issue_distribution = {
            category: len(problems) 
            for category, problems in issues.items()
        }
        
        # 개선 메트릭
        if len(validation_results) > 1:
            improvement_rate = (
                latest['quality_score'] - validation_results[0]['quality_score']
            ) / validation_results[0]['quality_score'] * 100
        else:
            improvement_rate = 0
        
        dashboard = {
            'current_quality': latest['quality_score'],
            'quality_trend': quality_trend,
            'issue_distribution': issue_distribution,
            'total_iterations': len(validation_results),
            'improvement_rate': improvement_rate,
            'recommendations': self.generate_improvement_recommendations(
                latest.get('final_validation', {})
            ),
            'quality_status': self._get_quality_status(latest['quality_score']),
            'automated_fixes_available': any(
                r.get('automated', False) 
                for r in self.generate_improvement_recommendations(
                    latest.get('final_validation', {})
                )
            )
        }
        
        return dashboard
    
    def _get_quality_status(self, quality_score: float) -> Dict[str, Any]:
        """품질 상태 분석"""
        if quality_score >= 0.9:
            status = 'excellent'
            message = '탁월한 품질'
            color = 'green'
        elif quality_score >= 0.8:
            status = 'good'
            message = '양호한 품질'
            color = 'blue'
        elif quality_score >= 0.7:
            status = 'acceptable'
            message = '수용 가능한 품질'
            color = 'yellow'
        elif quality_score >= 0.6:
            status = 'needs_improvement'
            message = '개선 필요'
            color = 'orange'
        else:
            status = 'poor'
            message = '품질 미달'
            color = 'red'
        
        return {
            'status': status,
            'message': message,
            'color': color,
            'score': quality_score
        }
    
    async def batch_quality_check(self, presentations: List[Presentation]) -> Dict[str, Any]:
        """여러 프레젠테이션 일괄 품질 검증"""
        logger.info(f"📊 일괄 품질 검증 시작: {len(presentations)}개 프레젠테이션")
        
        results = []
        total_issues = 0
        total_fixes = 0
        
        for i, prs in enumerate(presentations):
            logger.info(f"검증 중: {i+1}/{len(presentations)}")
            
            result = await self.validate_and_improve_presentation(prs)
            results.append({
                'presentation_index': i,
                'quality_score': result['final_quality_score'],
                'issues_resolved': result['total_issues_resolved'],
                'iterations': result['total_iterations']
            })
            
            total_issues += result['total_issues_resolved']
            total_fixes += result['total_issues_resolved']
        
        # 전체 통계
        avg_quality = sum(r['quality_score'] for r in results) / len(results)
        quality_distribution = {
            'excellent': len([r for r in results if r['quality_score'] >= 0.9]),
            'good': len([r for r in results if 0.8 <= r['quality_score'] < 0.9]),
            'acceptable': len([r for r in results if 0.7 <= r['quality_score'] < 0.8]),
            'needs_improvement': len([r for r in results if r['quality_score'] < 0.7])
        }
        
        batch_result = {
            'total_presentations': len(presentations),
            'average_quality': avg_quality,
            'quality_distribution': quality_distribution,
            'total_issues_resolved': total_issues,
            'individual_results': results,
            'processing_summary': {
                'presentations_improved': len([r for r in results if r['issues_resolved'] > 0]),
                'total_iterations': sum(r['iterations'] for r in results),
                'avg_iterations_per_presentation': sum(r['iterations'] for r in results) / len(results)
            }
        }
        
        logger.info(f"✅ 일괄 검증 완료: 평균 품질 {avg_quality:.3f}, 총 {total_issues}개 이슈 해결")
        
        return batch_result