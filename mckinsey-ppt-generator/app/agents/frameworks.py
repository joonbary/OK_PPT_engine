"""
McKinsey MECE 프레임워크 라이브러리
"""

from typing import Dict, List


class MECEFrameworkLibrary:
    """McKinsey 표준 MECE 프레임워크 컬렉션"""
    
    FRAMEWORKS = {
        '3C': {
            'name': '3C Analysis',
            'framework_name': '3C',
            'categories': ['Company', 'Competitors', 'Customers'],
            'description': '시장 진입 전략을 위한 3C 분석',
            'use_cases': ['market_entry', 'competitive_positioning'],
            'slide_allocation': {
                'Company': 3,
                'Competitors': 4,
                'Customers': 3
            }
        },
        'PORTER5': {
            'name': "Porter's 5 Forces",
            'framework_name': 'PORTER5',
            'categories': [
                '신규 진입자의 위협',
                '대체재의 위협',
                '구매자 교섭력',
                '공급자 교섭력',
                '기존 경쟁자 간 경쟁'
            ],
            'description': '산업 구조 분석 프레임워크',
            'use_cases': ['industry_analysis', 'competitive_strategy'],
            'slide_allocation': {
                '신규 진입자의 위협': 2,
                '대체재의 위협': 2,
                '구매자 교섭력': 2,
                '공급자 교섭력': 2,
                '기존 경쟁자 간 경쟁': 2
            }
        },
        'SWOT': {
            'name': 'SWOT Analysis',
            'framework_name': 'SWOT',
            'categories': ['Strengths', 'Weaknesses', 'Opportunities', 'Threats'],
            'description': '전략적 포지셔닝 분석',
            'use_cases': ['strategic_planning', 'business_assessment'],
            'slide_allocation': {
                'Strengths': 2,
                'Weaknesses': 2,
                'Opportunities': 3,
                'Threats': 3
            }
        },
        '7S': {
            'name': 'McKinsey 7S',
            'framework_name': '7S',
            'categories': [
                'Strategy',
                'Structure',
                'Systems',
                'Shared Values',
                'Skills',
                'Style',
                'Staff'
            ],
            'description': '조직 효과성 분석 프레임워크',
            'use_cases': ['organizational_change', 'performance_improvement'],
            'slide_allocation': {
                'Strategy': 2,
                'Structure': 2,
                'Systems': 2,
                'Shared Values': 1,
                'Skills': 1,
                'Style': 1,
                'Staff': 1
            }
        },
        '4P': {
            'name': 'Marketing Mix 4P',
            'framework_name': '4P',
            'categories': ['Product', 'Price', 'Place', 'Promotion'],
            'description': '마케팅 전략 수립 프레임워크',
            'use_cases': ['marketing_strategy', 'product_launch'],
            'slide_allocation': {
                'Product': 3,
                'Price': 2,
                'Place': 2,
                'Promotion': 3
            }
        },
        'CUSTOM': {
            'name': 'Custom MECE',
            'framework_name': 'CUSTOM',
            'categories': ['분석 영역 1', '분석 영역 2', '분석 영역 3'],
            'description': '커스텀 MECE 구조',
            'use_cases': ['custom_analysis'],
            'slide_allocation': {
                '분석 영역 1': 3,
                '분석 영역 2': 3,
                '분석 영역 3': 3
            }
        }
    }
    
    def get_framework(self, framework_key: str) -> Dict:
        """프레임워크 조회"""
        return self.FRAMEWORKS.get(framework_key, self.FRAMEWORKS['CUSTOM'])
    
    def list_frameworks(self) -> List[str]:
        """사용 가능한 프레임워크 목록"""
        return list(self.FRAMEWORKS.keys())
    
    def recommend_framework(self, context: str) -> str:
        """컨텍스트 기반 프레임워크 추천"""
        context_lower = context.lower()
        
        if '시장' in context_lower or 'market' in context_lower:
            return '3C'
        elif '경쟁' in context_lower or 'competitive' in context_lower:
            return 'PORTER5'
        elif '전략' in context_lower or 'strategy' in context_lower:
            return 'SWOT'
        elif '조직' in context_lower or 'organization' in context_lower:
            return '7S'
        elif '마케팅' in context_lower or 'marketing' in context_lower:
            return '4P'
        else:
            return 'CUSTOM'
