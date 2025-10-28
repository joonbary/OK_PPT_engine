"""
간단한 Actionability 테스트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.content_generator import ContentGenerator


def test_enhancement_methods():
    """강화 메서드 직접 테스트"""
    
    generator = ContentGenerator()
    
    # 1. 액션 아이템 생성 테스트
    print("=" * 60)
    print("1. 액션 아이템 생성 테스트")
    print("=" * 60)
    
    items = [
        "신제품 R&D 투자",
        "해외 시장 진출",
        "운영 효율 개선"
    ]
    
    action_items = generator._generate_action_items(items)
    print("\n원본:")
    for item in items:
        print(f"  - {item}")
    
    print("\n액션 강화:")
    for item in action_items:
        print(f"  - {item}")
    
    # 2. 우선순위 추가 테스트
    print("\n" + "=" * 60)
    print("2. 우선순위 추가 테스트")
    print("=" * 60)
    
    prioritized = generator._add_priorities(action_items)
    print("\n우선순위 추가:")
    for item in prioritized:
        print(f"  - {item}")
    
    # 3. 정량화 테스트
    print("\n" + "=" * 60)
    print("3. 정량화 테스트")
    print("=" * 60)
    
    quantified = generator._add_quantification(prioritized)
    print("\n정량화 추가:")
    for item in quantified:
        print(f"  - {item}")
    
    # 4. 전체 프로세스 테스트
    print("\n" + "=" * 60)
    print("4. 전체 강화 프로세스")
    print("=" * 60)
    
    original_bullets = [
        "매출 증가",
        "비용 절감",
        "고객 만족도 향상"
    ]
    
    enhanced = generator._enhance_bullet_points(original_bullets)
    
    print("\n원본 bullets:")
    for b in original_bullets:
        print(f"  - {b}")
        
    print("\n강화된 bullets:")
    for b in enhanced:
        print(f"  - {b}")
    
    # 5. 슬라이드 spec 강화 테스트
    print("\n" + "=" * 60)
    print("5. 슬라이드 spec 강화 테스트")
    print("=" * 60)
    
    slide_spec = {
        "content_type": "conclusion",
        "content": {
            "bullets": [
                "신규 사업 진출",
                "파트너십 강화",
                "디지털 전환"
            ]
        }
    }
    
    enhanced_spec = generator._enhance_actionability(slide_spec)
    
    print("\n원본 spec content:")
    print(slide_spec["content"])
    
    print("\n강화된 spec content:")
    print(enhanced_spec["content"])


if __name__ == "__main__":
    test_enhancement_methods()