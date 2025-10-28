# 📋 워드 파일 업로드 테스트 가이드

## 🎯 테스트 목적
워드(DOCX) 파일을 업로드하여 AI가 자동으로 PPT를 생성하는 기능을 검증합니다.

---

## 📝 방법 1: 웹 UI를 통한 테스트

### Step 1: 웹 인터페이스 접속
```
http://localhost:8080
```

### Step 2: 파일 업로드 UI 확인
웹 페이지에서 다음 요소들을 찾아보세요:
- "파일 선택" 또는 "Choose File" 버튼
- "Upload Document" 버튼
- 또는 드래그 앤 드롭 영역

### Step 3: 워드 파일 준비
1. **Microsoft Word로 새 문서 생성**
2. **아래 내용 복사-붙여넣기**:

```
글로벌 전기차 시장 진출 전략

1. 시장 현황
- 2025년 시장 규모: 8,500억 달러 (전년 대비 18% 성장)
- 아시아 시장 비중: 42% (3,570억 달러)
- 우리 회사 점유율: 현재 1.2%, 목표 3.5%

2. 핵심 전략
- 배터리 기술 우위 활용 (충전 속도 30% 빠름)
- 3개년 투자: 150억 달러 (R&D 60억, 마케팅 40억, 설비 50억)
- 기대 ROI: 180% (5년 누적)

3. 실행 계획
- Phase 1 (6개월): 시장 조사 및 파트너십
- Phase 2 (1년): 플래그십 모델 2종 출시
- Phase 3 (2년): 생산 3배 확대
- Phase 4 (3년): 프리미엄 라인 출시
```

3. **파일 저장**: `test_strategy.docx`로 저장

### Step 4: 파일 업로드 및 PPT 생성
1. 웹 페이지에서 파일 선택
2. `test_strategy.docx` 파일 선택
3. "Generate PPT" 버튼 클릭
4. 진행 상황 모니터링
5. 완료 후 PPT 다운로드

---

## 💻 방법 2: Python 스크립트를 통한 테스트

### 테스트 스크립트 생성
아래 Python 스크립트를 `test_word_upload.py`로 저장:

```python
import requests
import time
from pathlib import Path

def test_word_upload():
    """워드 파일 업로드 및 PPT 생성 테스트"""
    
    # 1. 워드 파일 업로드
    print("1. Uploading Word document...")
    
    # 파일 경로 (실제 워드 파일 경로로 변경)
    file_path = "test_strategy.docx"
    
    if not Path(file_path).exists():
        print(f"Error: File {file_path} not found!")
        print("Please create a Word document first.")
        return
    
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
        response = requests.post('http://localhost:8000/api/v1/upload-document', files=files)
    
    if response.status_code != 200:
        print(f"Upload failed: {response.status_code}")
        print(response.text)
        return
    
    result = response.json()
    print(f"Upload successful!")
    print(f"- Filename: {result['filename']}")
    print(f"- File size: {result['file_size']} bytes")
    print(f"- Extracted text length: {len(result['text'])} characters")
    
    # 2. PPT 생성 요청
    print("\n2. Requesting PPT generation...")
    
    ppt_request = {
        "document": result['text'],
        "num_slides": 10,
        "target_audience": "Executive Board"
    }
    
    response = requests.post('http://localhost:8000/api/v1/generate-ppt', json=ppt_request)
    
    if response.status_code != 200:
        print(f"PPT generation request failed: {response.status_code}")
        return
    
    ppt_id = response.json()['ppt_id']
    print(f"PPT ID: {ppt_id}")
    
    # 3. 상태 추적
    print("\n3. Tracking generation progress...")
    
    for i in range(120):  # 최대 2분 대기
        response = requests.get(f'http://localhost:8000/api/v1/ppt-status/{ppt_id}')
        if response.status_code == 200:
            data = response.json()
            status = data['status']
            progress = data['progress']
            stage = data.get('current_stage', 'N/A')
            
            print(f"\r[{progress:3}%] Status: {status}, Stage: {stage}", end='')
            
            if status == 'completed':
                print(f"\n\nPPT Generation Complete!")
                print(f"Download URL: http://localhost:8000{data['download_url']}")
                print(f"Quality Score: {data.get('quality_score', 'N/A')}")
                
                # 4. PPT 다운로드
                download_url = f"http://localhost:8000{data['download_url']}"
                response = requests.get(download_url)
                
                if response.status_code == 200:
                    output_file = f"generated_from_word_{ppt_id[:8]}.pptx"
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                    print(f"\nPPT saved as: {output_file}")
                
                break
            elif status == 'failed':
                print(f"\n\nGeneration failed: {data.get('error', 'Unknown error')}")
                break
        
        time.sleep(1)

if __name__ == "__main__":
    test_word_upload()
```

### 스크립트 실행
```bash
python test_word_upload.py
```

---

## 🔨 방법 3: cURL 명령어를 통한 테스트

### Step 1: 워드 파일 업로드
```bash
# 파일 업로드 및 텍스트 추출
curl -X POST "http://localhost:8000/api/v1/upload-document" \
  -F "file=@test_strategy.docx" \
  > upload_result.json

# 결과 확인
cat upload_result.json
```

### Step 2: 추출된 텍스트로 PPT 생성
```bash
# upload_result.json에서 text 필드를 복사하여 사용
curl -X POST "http://localhost:8000/api/v1/generate-ppt" \
  -H "Content-Type: application/json" \
  -d '{
    "document": "추출된 텍스트 여기에 붙여넣기",
    "num_slides": 10,
    "target_audience": "Executive Board"
  }'
```

---

## 🧪 테스트 체크리스트

### 파일 업로드 검증
- [ ] DOCX 파일 업로드 성공
- [ ] 텍스트 추출 확인
- [ ] 파일 크기 제한 (10MB) 확인
- [ ] 지원하지 않는 형식 에러 처리

### PPT 생성 검증
- [ ] AI가 워드 내용을 분석하여 헤드라인 생성
- [ ] 적절한 슬라이드 수 생성 (5-15개)
- [ ] McKinsey 스타일 적용
- [ ] 차트/그래프 데이터 추출 및 시각화

### 품질 검증
- [ ] 품질 점수 0.85 이상
- [ ] 원문 내용 정확 반영
- [ ] 논리적 구조 유지
- [ ] 정량화된 데이터 보존

---

## 📊 예상 결과

### 성공적인 업로드 응답
```json
{
  "success": true,
  "text": "글로벌 전기차 시장 진출 전략...",
  "filename": "test_strategy.docx",
  "file_size": 15234,
  "format": "docx"
}
```

### 성공적인 PPT 생성
- 10-12개 슬라이드 생성
- 각 슬라이드에 AI 생성 헤드라인
- 주요 수치 (8,500억, 180% ROI 등) 반영
- McKinsey 스타일 (파란색 테마)

---

## 🚨 문제 해결

### 파일 업로드 실패
1. 파일 형식 확인 (.docx, .pdf, .md만 지원)
2. 파일 크기 확인 (10MB 이하)
3. 서버 상태 확인 (`docker-compose ps`)

### PPT 생성 실패
1. 문서 내용이 너무 짧음 (최소 100자 이상 권장)
2. Redis 서버 확인
3. OpenAI API 키 확인

### 다운로드 실패
1. PPT ID 확인
2. 생성 완료 여부 확인
3. 파일 경로 권한 확인

---

## 📁 테스트 파일 위치

- 워드 파일: `D:\PPT_Designer_OK\test_strategy.docx`
- 생성된 PPT: `D:\PPT_Designer_OK\generated_*.pptx`
- 테스트 스크립트: `D:\PPT_Designer_OK\test_word_upload.py`

---

**준비 완료!** 위 방법 중 하나를 선택하여 테스트를 진행하세요.