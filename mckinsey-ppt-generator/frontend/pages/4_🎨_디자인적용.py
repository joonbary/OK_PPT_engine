# D:\PPT_Designer_OK\mckinsey-ppt-generator\frontend\pages\4_🎨_디자인적용.py

import streamlit as st
import sys
import os
import time
from PIL import Image

# 프로젝트 루트 경로 설정
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from frontend.components.progress_tracker import render_progress_tracker

# --- Mock/Placeholder Implementations ---
class DesignApplicator:
    """디자인을 적용하고 슬라이드를 검증하는 가상 Applicator"""
    def apply_design(self, all_slides_content):
        # stage4.txt의 요구사항에 따라 모의 데이터를 생성합니다.
        # 실제로는 python-pptx를 사용하여 PPT를 생성합니다.
        process_log = [
            ("템플릿 적용", 1),
            ("폰트/색상 표준화", 1),
            (f"차트 생성 ({len(all_slides_content)}개)", 2),
            ("디자인 요소 검증", 1)
        ]
        validation_results = {
            "text_overflow": {"found": 1, "fixed": 1},
            "element_overlap": {"found": 0, "fixed": 0},
            "readability_score": 0.98
        }
        # 모의 PPTX 파일 경로 및 미리보기 이미지 생성
        output_path = os.path.join(project_root, "output", "generated_presentation_mock.pptx")
        # Create a dummy file to simulate output
        with open(output_path, "w") as f:
            f.write("This is a mock PPTX file.")
            
        return {
            "process_log": process_log,
            "validation_results": validation_results,
            "output_pptx_path": output_path,
            "preview_images": [Image.new('RGB', (400, 300), color = 'rgb(240, 240, 240)') for _ in all_slides_content]
        }

# --- Streamlit UI ---
st.set_page_config(page_title="Stage 4: 디자인 적용", page_icon="🎨", layout="wide")

st.title("🎨 Stage 4: 디자인 적용")
render_progress_tracker(current_stage=4)

# Stage 3 결과 확인
if 'stage3_result' not in st.session_state or not st.session_state['stage3_result']:
    st.warning("⚠️ Stage 3: 콘텐츠 생성을 먼저 완료해주세요.")
    st.page_link("pages/3_✍️_콘텐츠생성.py", label="Stage 3으로 이동")
    st.stop()

# 세션 상태 초기화
if 'stage4_result' not in st.session_state:
    st.session_state['stage4_result'] = None

# 디자인 적용 버튼
st.info("생성된 콘텐츠에 McKinsey 디자인 템플릿을 적용하고, 슬라이드를 최종 검증합니다.")
if st.button("🎨 디자인 적용 및 검증 시작", type="primary"):
    applicator = DesignApplicator()
    
    # 가상 프로세스 실행
    mock_process_log = applicator.apply_design(st.session_state['stage3_result'])['process_log']
    status_area = st.empty()
    for i, (task, duration) in enumerate(mock_process_log):
        status_area.info(f"🔄 {task} 중...")
        time.sleep(duration)
        status_area.success(f"✅ {task} 완료!")
    
    # 결과 저장
    st.session_state['stage4_result'] = applicator.apply_design(st.session_state['stage3_result'])
    st.success("✅ 모든 디자인 적용 및 검증 완료!")

# 디자인 적용 결과 표시
if st.session_state['stage4_result']:
    st.markdown("--- ")
    st.subheader("디자인 적용 및 검증 결과")
    result = st.session_state['stage4_result']
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📊 슬라이드 미리보기")
        # 썸네일 그리드
        total_slides = len(result['preview_images'])
        cols = st.columns(5)
        for i in range(total_slides):
            with cols[i % 5]:
                st.image(result['preview_images'][i], caption=f"Slide {i+1}", use_column_width=True)
                if st.button(f"상세보기 {i+1}", key=f"detail_{i}"):
                    st.toast(f"Slide {i+1} 상세 보기 기능은 개발 중입니다.")

    with col2:
        st.subheader("🔍 자동 검증 및 수정 로그")
        validation = result['validation_results']
        st.write(f"- **텍스트 오버플로우:** {validation['text_overflow']['found']}건 발견, {validation['text_overflow']['fixed']}건 자동 수정 완료")
        st.write(f"- **요소 겹침:** {validation['element_overlap']['found']}건 발견, {validation['element_overlap']['fixed']}건 자동 수정 완료")
        st.metric(label="가독성 점수", value=f"{validation['readability_score'] * 100:.1f}%")

    # 다음 단계로 이동 버튼
    st.markdown("--- ")
    if st.button("→ Stage 5: 품질 검토로 이동", type="primary"):
        st.switch_page("pages/5_✅_품질검토.py")
