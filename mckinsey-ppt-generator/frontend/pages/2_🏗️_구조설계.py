# D:\PPT_Designer_OK\mckinsey-ppt-generator\frontend\pages\2_🏗️_구조설계.py

import streamlit as st
import sys
import os

# 프로젝트 루트 경로 설정
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from frontend.components.progress_tracker import render_progress_tracker

# --- Mock/Placeholder Implementations ---
class StorytellerAgent:
    """프레젠테이션 구조를 설계하는 가상 StorytellerAgent"""
    def design_structure(self, analysis_result, framework, num_slides):
        # stage2.txt의 JSON 구조에 따라 모의 데이터를 생성합니다.
        return {
            "framework": framework,
            "total_slides": num_slides,
            "story_structure": "SCR", # Situation, Complication, Resolution
            "slide_outline": [
                {"slide_number": 1, "type": "title", "layout": "TitleSlide", "headline": f"{analysis_result['key_topics'][0]} 관련 제안"},
                {"slide_number": 2, "type": "executive_summary", "layout": "DualHeader", "headline": f"핵심 결론: {analysis_result['core_message']}"},
                {"slide_number": 3, "type": "situation", "layout": "ThreeColumn", "headline": "현재 상황(Situation): 시장 기회 분석"},
                {"slide_number": 4, "type": "complication", "layout": "Standard", "headline": "과제(Complication): 해결해야 할 문제점"},
                {"slide_number": 5, "type": "resolution", "layout": "TwoColumn", "headline": "해결 방안(Resolution): 구체적 실행 전략"},
            ] + [
                {"slide_number": i, "type": f"detail_{i-5}", "layout": "Standard", "headline": f"세부 내용 #{i-5}"} for i in range(6, num_slides + 1)
            ]
        }

# --- Streamlit UI ---
st.set_page_config(page_title="Stage 2: 구조 설계", page_icon="🏗️", layout="wide")

st.title("🏗️ Stage 2: 구조 설계")
render_progress_tracker(current_stage=2)

# Stage 1 결과 확인
if 'stage1_result' not in st.session_state or st.session_state['stage1_result'] is None:
    st.warning("⚠️ Stage 1: 문서 분석을 먼저 완료해주세요.")
    st.page_link("pages/1_📄_문서분석.py", label="Stage 1으로 이동")
    st.stop()

# 세션 상태 초기화
if 'stage2_result' not in st.session_state:
    st.session_state['stage2_result'] = None

# 구조 설계 옵션
st.subheader("구조 설계 옵션")
col1, col2 = st.columns(2)
with col1:
    framework_options = ["3C", "4P", "SWOT", "Porter's 5 Forces", "커스텀"]
    selected_framework = st.selectbox("분석 프레임워크 선택", framework_options)
with col2:
    num_slides = st.slider("목표 슬라이드 수", min_value=5, max_value=20, value=10)

# 구조 생성 버튼
if st.button("🏗️ 구조 생성", type="primary"):
    with st.spinner("AI가 프레젠테이션 구조를 설계 중입니다..."):
        storyteller = StorytellerAgent()
        structure_result = storyteller.design_structure(
            st.session_state['stage1_result'],
            selected_framework,
            num_slides
        )
        st.session_state['stage2_result'] = structure_result
        st.success("✅ 구조 설계 완료!")

# 구조 설계 결과 표시
if st.session_state['stage2_result']:
    st.markdown("--- ")
    st.subheader("AI가 설계한 슬라이드 구조")
    result = st.session_state['stage2_result']
    
    st.info(f"**선택된 프레임워크:** {result['framework']} | **총 슬라이드:** {result['total_slides']}장 | **스토리 구조:** {result['story_structure']}")

    # 슬라이드 아웃라인 (수정 가능하게)
    for i, slide in enumerate(result['slide_outline']):
        with st.expander(f"**Slide {slide['slide_number']}: [{slide['type']}]** {slide['headline']}"):
            new_headline = st.text_input("헤드라인 수정", value=slide['headline'], key=f"headline_{i}")
            slide['headline'] = new_headline # 세션 상태 직접 업데이트
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**레이아웃:** {slide['layout']}")
            with col2:
                if st.button("🎨 레이아웃 미리보기", key=f"preview_{i}"):
                    st.toast(f"'{slide['layout']}' 레이아웃 미리보기 기능은 개발 중입니다.")

    # 다음 단계로 이동 버튼
    if st.button("→ Stage 3: 콘텐츠 생성으로 이동", type="primary"):
        st.switch_page("pages/3_✍️_콘텐츠생성.py")
