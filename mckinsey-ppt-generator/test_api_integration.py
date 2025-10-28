"""
FastAPI 통합 테스트 스크립트
API 엔드포인트를 통해 PPT 생성 시스템을 테스트합니다.
"""

import requests
import json
import time
from pathlib import Path


# API 서버 주소
API_BASE_URL = "http://localhost:8000"
# 인증 토큰 (필요시 사용)
AUTH_TOKEN = None
# 테스트용 헤더
HEADERS = {}


def test_register_and_login():
    """테스트 사용자 등록 및 로그인"""
    global AUTH_TOKEN, HEADERS
    print("\n0. 테스트 사용자 등록 및 로그인...")
    
    # 테스트 사용자 정보
    test_password = "Test1234!"  # 대문자, 소문자, 숫자, 특수문자 포함
    test_user = {
        "username": "test_user",
        "email": "test@example.com",
        "password": test_password,
        "password_confirm": test_password,  # 비밀번호 확인 필드
        "full_name": "Test User"
    }
    
    # 1. 회원가입 시도
    print("   회원가입 시도...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/auth/register",
            json=test_user
        )
        print(f"   회원가입 응답 코드: {response.status_code}")
        if response.status_code == 201:
            print("   [SUCCESS] 회원가입 성공")
        elif response.status_code == 400:
            print("   [INFO] 이미 등록된 사용자")
            print(f"   상세: {response.text}")
        else:
            print(f"   [ERROR] 회원가입 실패: {response.status_code}")
            print(f"   상세: {response.text}")
    except Exception as e:
        print(f"   [ERROR] 회원가입 실패: {str(e)}")
    
    # 2. 로그인
    print("   로그인 시도...")
    try:
        # OAuth2 형식으로 전송
        login_data = {
            "username": test_user["email"],  # 이메일로 로그인
            "password": test_password,  # 비밀번호
            "grant_type": "password"  # OAuth2 필수 필드
        }
        response = requests.post(
            f"{API_BASE_URL}/api/v1/auth/login",
            data=login_data  # form-data로 전송
        )
        
        if response.status_code == 200:
            result = response.json()
            AUTH_TOKEN = result.get("access_token")
            HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}
            print("   [SUCCESS] 로그인 성공")
            print(f"   - 토큰 타입: {result.get('token_type', 'N/A')}")
            return True
        else:
            print(f"   [ERROR] 로그인 실패: {response.status_code}")
            print(f"   오류: {response.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] 로그인 실패: {str(e)}")
        return False


def test_health_check():
    """서버 상태 확인"""
    print("\n1. 서버 상태 확인...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("   [OK] 서버가 정상 작동 중입니다.")
            print(f"   응답: {response.json()}")
            return True
        else:
            print(f"   [ERROR] 서버 응답 오류: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   [ERROR] 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        print("   실행 명령: uvicorn app.main:app --reload")
        return False


def test_generate_ppt_from_markdown():
    """마크다운으로 PPT 생성 테스트"""
    print("\n2. 마크다운으로 PPT 생성 테스트...")
    
    # 테스트 마크다운 콘텐츠
    markdown_content = """# 디지털 전환 전략 2024

## 핵심 목표

### 1. 시장 점유율 확대
- 현재 시장 점유율: 15%
- 목표 시장 점유율: 25%
- 신규 고객 획득: 10,000명
- 기존 고객 유지율: 95%

### 2. 디지털 채널 강화
- 모바일 앱 사용자 증가
- 온라인 매출 비중 확대
- AI 챗봇 도입
- 개인화 마케팅 강화

### 3. 운영 효율성 개선
- 자동화 프로세스 도입
- 클라우드 마이그레이션
- 데이터 분석 플랫폼 구축
- 실시간 대시보드 구현

## 실행 계획

### Phase 1: 기반 구축 (Q1-Q2)
- 인프라 현대화
- 팀 역량 강화
- 파일럿 프로젝트 실행

### Phase 2: 확산 (Q3-Q4)
- 전사 롤아웃
- 성과 측정 및 개선
- 차년도 계획 수립

## 기대 효과
**매출 증대**: 30% 성장 예상
**비용 절감**: 운영비 20% 감소
**고객 만족**: NPS 80점 달성
"""
    
    # Form 데이터로 전송
    form_data = {
        "markdown_content": markdown_content,
        "title": "디지털 전환 전략 2024",
        "template": "McKinsey Professional"
    }
    
    try:
        # PPT 생성 요청 - 올바른 엔드포인트 사용
        print("   요청 전송 중...")
        response = requests.post(
            f"{API_BASE_URL}/api/v1/markdown/convert",
            data=form_data,  # form-data로 전송
            headers=HEADERS  # 인증 헤더 추가
        )
        
        if response.status_code == 200:
            result = response.json()
            print("   [SUCCESS] PPT 생성 성공!")
            print(f"   - 프레젠테이션 ID: {result.get('presentation_id', 'N/A')}")
            print(f"   - 슬라이드 수: {result.get('slide_count', 0)}")
            print(f"   - 다운로드 URL: {result.get('download_url', 'N/A')}")
            print(f"   - 메시지: {result.get('message', '')}")
                
            return result.get('presentation_id')
        else:
            print(f"   [ERROR] 생성 실패: {response.status_code}")
            print(f"   오류: {response.text}")
            return None
            
    except Exception as e:
        print(f"   [ERROR] 요청 실패: {str(e)}")
        return None


def test_get_presentation_info(presentation_id):
    """생성된 프레젠테이션 정보 조회"""
    if not presentation_id:
        return
    
    print(f"\n3. 프레젠테이션 정보 조회 (ID: {presentation_id})...")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/v1/presentations/{presentation_id}",
            headers=HEADERS  # 인증 헤더 추가
        )
        
        if response.status_code == 200:
            info = response.json()
            print("   [SUCCESS] 조회 성공!")
            print(f"   - 제목: {info.get('title', 'N/A')}")
            print(f"   - 생성 시간: {info.get('created_at', 'N/A')}")
            print(f"   - 슬라이드 수: {info.get('slide_count', 0)}")
            print(f"   - AI 모델: {info.get('ai_model', 'N/A')}")
            
            # 슬라이드 정보
            if 'slides' in info:
                print(f"\n   [SLIDES] 슬라이드 목록:")
                for slide in info['slides'][:5]:  # 처음 5개만 표시
                    print(f"   - 슬라이드 {slide.get('slide_number', 0)}: {slide.get('title', 'N/A')}")
                    print(f"     레이아웃: {slide.get('layout_type', 'N/A')}")
        else:
            print(f"   [ERROR] 조회 실패: {response.status_code}")
            
    except Exception as e:
        print(f"   [ERROR] 요청 실패: {str(e)}")


def test_download_presentation(presentation_id):
    """생성된 PPT 파일 다운로드"""
    if not presentation_id:
        return
    
    print(f"\n4. PPT 파일 다운로드 (ID: {presentation_id})...")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/v1/presentations/{presentation_id}/download",
            headers=HEADERS  # 인증 헤더 추가
        )
        
        if response.status_code == 200:
            # 파일 저장
            filename = f"downloaded_presentation_{presentation_id}.pptx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"   [SUCCESS] 다운로드 성공!")
            print(f"   - 파일명: {filename}")
            print(f"   - 파일 크기: {len(response.content):,} bytes")
        else:
            print(f"   [ERROR] 다운로드 실패: {response.status_code}")
            
    except Exception as e:
        print(f"   [ERROR] 요청 실패: {str(e)}")


def test_ai_enhancement():
    """AI 콘텐츠 개선 테스트 - 현재 미구현"""
    print("\n5. AI 콘텐츠 개선 테스트...")
    print("   [INFO] AI 엔드포인트는 아직 구현되지 않았습니다.")
    print("   [INFO] 향후 OpenAI/Claude API 통합 예정입니다.")
    
    # AI 개선 기능이 구현되면 활성화할 코드
    # content = {
    #     "title": "판매 실적",
    #     "content": "판매가 증가했음. 좋은 성과. 계속 노력 필요."
    # }
    # 
    # request_data = {
    #     "content": content,
    #     "enhancement_type": "professional",
    #     "language": "ko"
    # }
    # 
    # try:
    #     response = requests.post(
    #         f"{API_BASE_URL}/api/v1/ai/enhance-content",
    #         json=request_data
    #     )
    #     
    #     if response.status_code == 200:
    #         result = response.json()
    #         print("   [SUCCESS] AI 개선 성공!")
    #         print(f"\n   원본 콘텐츠:")
    #         print(f"   {content['content']}")
    #         print(f"\n   개선된 콘텐츠:")
    #         print(f"   {result.get('enhanced_content', {}).get('content', 'N/A')}")
    #     else:
    #         print(f"   [ERROR] AI 개선 실패: {response.status_code}")
    #         
    # except Exception as e:
    #     print(f"   [ERROR] 요청 실패: {str(e)}")


def run_all_api_tests():
    """모든 API 테스트 실행"""
    print("\n" + "="*60)
    print(" FastAPI 통합 테스트")
    print("="*60)
    
    # 1. 서버 상태 확인
    if not test_health_check():
        print("\n[WARNING] 서버가 실행되지 않았습니다.")
        print("다음 명령으로 서버를 실행하세요:")
        print("cd mckinsey-ppt-generator")
        print("uvicorn app.main:app --reload")
        return
    
    # 2. 사용자 등록 및 로그인
    if not test_register_and_login():
        print("\n[ERROR] 인증에 실패했습니다.")
        return
    
    # 3. PPT 생성
    presentation_id = test_generate_ppt_from_markdown()
    
    # 4. 프레젠테이션 정보 조회
    test_get_presentation_info(presentation_id)
    
    # 5. PPT 다운로드
    test_download_presentation(presentation_id)
    
    # 6. AI 개선 테스트 (현재 미구현)
    test_ai_enhancement()
    
    print("\n" + "="*60)
    print(" [SUCCESS] API 테스트 완료!")
    print("="*60)


if __name__ == "__main__":
    run_all_api_tests()