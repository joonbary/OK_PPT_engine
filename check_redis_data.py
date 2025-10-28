"""
Redis에서 PPT 생성 데이터 확인
"""

import redis
import json

def check_redis_data():
    """Redis에서 최근 PPT 생성 데이터 확인"""
    
    try:
        # Redis 연결
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        
        print("="*60)
        print("Redis PPT Data Check")
        print("="*60)
        
        # 최근 PPT ID 찾기
        ppt_id = "bb5ab511-3a9c-4e6f-a1f9-81aa45b50e8a"
        
        # 1. PPT 상태 확인
        status_key = f"ppt_status:{ppt_id}"
        status_data = r.get(status_key)
        
        if status_data:
            status = json.loads(status_data)
            print(f"\nPPT Status: {status.get('status')}")
            print(f"Quality Score: {status.get('quality_score')}")
            print(f"Current Stage: {status.get('current_stage')}")
        else:
            print(f"No status data for PPT ID: {ppt_id}")
        
        # 2. 워크플로우 결과 확인
        workflow_key = f"workflow_result:{ppt_id}"
        workflow_data = r.get(workflow_key)
        
        if workflow_data:
            print("\n" + "-"*40)
            print("Workflow Result Found!")
            
            result = json.loads(workflow_data)
            
            # 슬라이드 데이터 확인
            if 'slides' in result:
                slides = result['slides']
                print(f"Total slides in workflow: {len(slides)}")
                
                # 첫 3개 슬라이드 헤드라인 확인
                print("\nFirst 3 slide headlines from workflow:")
                for i, slide in enumerate(slides[:3], 1):
                    headline = slide.get('headline', 'No headline')
                    # ASCII로 변환 가능한 문자만 출력
                    safe_headline = ''.join(c if ord(c) < 128 else '?' for c in headline)
                    print(f"  Slide {i}: {safe_headline[:60]}")
                    
                    # headline 필드가 있는지 확인
                    if 'headline' in slide:
                        print(f"    -> Has 'headline' field: YES")
                    else:
                        print(f"    -> Has 'headline' field: NO")
            else:
                print("No slides data in workflow result")
        else:
            print("\n[WARNING] No workflow result found in Redis!")
            print("This means the AI workflow data is not being saved.")
        
        # 3. 생성된 PPT 파일 경로 확인
        file_key = f"ppt_file:{ppt_id}"
        file_path = r.get(file_key)
        
        if file_path:
            print(f"\n" + "-"*40)
            print(f"PPT File Path: {file_path}")
        
        # 4. 모든 관련 키 확인
        print("\n" + "-"*40)
        print("All Redis keys for this PPT:")
        
        all_keys = r.keys(f"*{ppt_id}*")
        for key in all_keys:
            print(f"  - {key}")
            
        # 5. styled_slides 데이터 확인
        styled_key = f"styled_slides:{ppt_id}"
        styled_data = r.get(styled_key)
        
        if styled_data:
            print("\n" + "-"*40)
            print("Styled Slides Data Found!")
            styled = json.loads(styled_data)
            
            if isinstance(styled, list):
                print(f"Total styled slides: {len(styled)}")
                
                # 첫 번째 슬라이드 구조 확인
                if styled:
                    first_slide = styled[0]
                    print(f"\nFirst slide structure:")
                    print(f"  Keys: {list(first_slide.keys())}")
                    
                    # headline vs title 확인
                    has_headline = 'headline' in first_slide
                    has_title = 'title' in first_slide
                    
                    print(f"  Has 'headline': {has_headline}")
                    print(f"  Has 'title': {has_title}")
                    
                    if has_headline:
                        headline = first_slide['headline']
                        safe_text = ''.join(c if ord(c) < 128 else '?' for c in headline)
                        print(f"  Headline: {safe_text[:60]}")
                    
                    if has_title:
                        title = first_slide['title']
                        safe_text = ''.join(c if ord(c) < 128 else '?' for c in title)
                        print(f"  Title: {safe_text[:60]}")
        else:
            print("\n[WARNING] No styled_slides data found!")
            
    except redis.ConnectionError:
        print("[ERROR] Cannot connect to Redis")
        print("Make sure Redis is running in Docker")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    check_redis_data()