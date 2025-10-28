"""
워드 파일 업로드 및 PPT 생성 테스트 스크립트
"""

import requests
import time
from pathlib import Path
from datetime import datetime

def test_word_upload():
    """워드 파일 업로드 및 PPT 생성 테스트"""
    
    print("="*60)
    print("Word Document Upload & PPT Generation Test")
    print("="*60)
    
    # 1. 워드 파일 업로드
    print("\n1. Uploading Word document...")
    
    # 테스트할 파일 목록 (md 파일로 테스트)
    test_files = [
        "test_document.md",  # 먼저 MD 파일로 테스트
        # "test_strategy.docx"  # 실제 워드 파일이 있으면 이 주석 제거
    ]
    
    for file_path in test_files:
        if Path(file_path).exists():
            print(f"\nTesting with file: {file_path}")
            test_single_file(file_path)
            break
    else:
        print("No test files found!")
        print("Please create one of these files:")
        for f in test_files:
            print(f"  - {f}")

def test_single_file(file_path):
    """단일 파일 테스트"""
    
    try:
        # 파일 업로드
        with open(file_path, 'rb') as f:
            # 파일 확장자에 따른 MIME 타입 설정
            if file_path.endswith('.docx'):
                mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif file_path.endswith('.pdf'):
                mime_type = 'application/pdf'
            else:  # .md
                mime_type = 'text/markdown'
            
            files = {'file': (file_path, f, mime_type)}
            response = requests.post('http://localhost:8000/api/v1/upload-document', files=files)
        
        if response.status_code != 200:
            print(f"[ERROR] Upload failed: {response.status_code}")
            print(response.text)
            return
        
        result = response.json()
        print(f"[SUCCESS] Upload successful!")
        print(f"  - Filename: {result['filename']}")
        print(f"  - File size: {result['file_size']:,} bytes")
        print(f"  - Format: {result['format']}")
        print(f"  - Extracted text length: {len(result['text']):,} characters")
        
        # 텍스트 미리보기
        preview_text = result['text'][:200] + "..." if len(result['text']) > 200 else result['text']
        print(f"\nText preview:")
        print("-"*40)
        print(preview_text)
        print("-"*40)
        
        # 2. PPT 생성 요청
        print("\n2. Requesting PPT generation...")
        
        ppt_request = {
            "document": result['text'],
            "num_slides": 10,
            "target_audience": "Executive Board"
        }
        
        response = requests.post('http://localhost:8000/api/v1/generate-ppt', json=ppt_request)
        
        if response.status_code != 200:
            print(f"[ERROR] PPT generation request failed: {response.status_code}")
            print(response.text)
            return
        
        ppt_id = response.json()['ppt_id']
        print(f"[SUCCESS] PPT ID: {ppt_id}")
        
        # 3. 상태 추적
        print("\n3. Tracking generation progress...")
        print("-"*40)
        
        start_time = time.time()
        last_stage = None
        
        for i in range(120):  # 최대 2분 대기
            response = requests.get(f'http://localhost:8000/api/v1/ppt-status/{ppt_id}')
            if response.status_code == 200:
                data = response.json()
                status = data['status']
                progress = data['progress']
                stage = data.get('current_stage', 'N/A')
                
                # 단계 변경 시 새 줄 출력
                if stage != last_stage:
                    if last_stage is not None:
                        print()  # 이전 줄 완료
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"[{timestamp}] Stage: {stage}")
                    last_stage = stage
                
                # 프로그레스 바
                bar_length = 30
                filled = int(bar_length * progress / 100)
                bar = '#' * filled + '-' * (bar_length - filled)
                
                print(f"\r  [{bar}] {progress:3}% | {status}", end='')
                
                if status == 'completed':
                    print()  # 줄바꿈
                    print("-"*40)
                    print(f"\n[SUCCESS] PPT Generation Complete!")
                    print(f"  - Total time: {time.time() - start_time:.1f} seconds")
                    print(f"  - Quality Score: {data.get('quality_score', 'N/A')}")
                    print(f"  - Download URL: http://localhost:8000{data['download_url']}")
                    
                    # 4. PPT 다운로드
                    print("\n4. Downloading PPT file...")
                    download_url = f"http://localhost:8000{data['download_url']}"
                    response = requests.get(download_url)
                    
                    if response.status_code == 200:
                        output_file = f"generated_from_{Path(file_path).stem}_{ppt_id[:8]}.pptx"
                        with open(output_file, 'wb') as f:
                            f.write(response.content)
                        print(f"[SUCCESS] PPT saved as: {output_file}")
                        print(f"  - File size: {len(response.content):,} bytes")
                        
                        # 성공 요약
                        print("\n" + "="*60)
                        print("TEST COMPLETED SUCCESSFULLY!")
                        print("="*60)
                        print(f"Input: {file_path}")
                        print(f"Output: {output_file}")
                        print(f"Quality: {data.get('quality_score', 'N/A')}")
                        print(f"Time: {time.time() - start_time:.1f}s")
                    else:
                        print(f"[ERROR] Download failed: {response.status_code}")
                    
                    break
                    
                elif status == 'failed':
                    print()  # 줄바꿈
                    print(f"\n[ERROR] Generation failed: {data.get('error', 'Unknown error')}")
                    break
            
            time.sleep(1)
        else:
            print("\n[ERROR] Timeout: Generation took too long")
            
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()

def check_server_status():
    """서버 상태 확인"""
    print("\nChecking server status...")
    
    try:
        # API 서버 확인
        response = requests.get('http://localhost:8000/api/v1/supported-formats')
        if response.status_code == 200:
            data = response.json()
            print("[OK] API Server is running")
            print(f"  - Supported formats: {', '.join(data['formats'])}")
            print(f"  - Max file size: {data['max_size_mb']} MB")
        else:
            print("[ERROR] API Server not responding properly")
            
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to API server at http://localhost:8000")
        print("Please ensure Docker containers are running:")
        print("  docker-compose ps")
        return False
    
    return True

if __name__ == "__main__":
    # 서버 상태 확인
    if check_server_status():
        # 테스트 실행
        test_word_upload()
    else:
        print("\nPlease fix server issues before running tests.")