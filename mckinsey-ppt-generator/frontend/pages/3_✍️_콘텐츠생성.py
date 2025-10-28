# D:\PPT_Designer_OK\mckinsey-ppt-generator\frontend\pages\3_✍️_콘텐츠생성.py

import streamlit as st
import sys
import os
import time

# 프로젝트 루트 경로 설정
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from frontend.components.progress_tracker import render_progress_tracker

# --- Mock/Placeholder Implementations ---
class ContentGenerator:
    """슬라이드 콘텐츠를 생성하는 가상 ContentGenerator"""
    def generate_slide_content(self, slide_info):
        # stage3.txt의 JSON 구조에 따라 모의 데이터를 생성합니다.
        headline = slide_info['headline']
        return {
            "slide_number": slide_info['slide_number'],
            "headline": f"{headline} (상세 내용)",
            "content": {
                "insight_level_1": f"({headline}) 관련 첫 번째 인사이트입니다.",
                "insight_level_2": f"({headline}) 관련 두 번째 심층 분석입니다.",
                "insight_level_3": f"({headline}) 관련 세 번째 전략적 제언입니다.",
                "insight_level_4": f"({headline}) 관련 최종 실행 방안입니다.",
                "body_points": [
                    "핵심 논거 1: 관련 데이터와 근거를 제시합니다.",
                    "핵심 논거 2: 시장 동향과 연관성을 설명합니다."
                ],
                "action_items": [
                    "[최우선] 가장 시급하고 중요한 실행 과제입니다.",
                    "[핵심] 차순위로 진행해야 할 핵심 과제입니다."
                ]
            }
        }

# --- Streamlit UI ---
st.set_page_config(page_title="Stage 3: 콘텐츠 생성", page_icon="✍️", layout="wide")

st.title("✍️ Stage 3: 콘텐츠 생성")
render_progress_tracker(current_stage=3)

# Stage 2 결과 확인
if 'stage2_result' not in st.session_state or st.session_state['stage2_result'] is None:
    st.warning("⚠️ Stage 2: 구조 설계를 먼저 완료해주세요.")
    st.page_link("pages/2_🏗️_구조설계.py", label="Stage 2로 이동")
    st.stop()

# 세션 상태 초기화
if 'stage3_result' not in st.session_state:
    st.session_state['stage3_result'] = {}

# 콘텐츠 생성 버튼
st.info("설계된 구조에 따라 각 슬라이드의 상세 콘텐츠를 AI가 생성합니다.")
if st.button("✍️ 콘텐츠 생성 시작", type="primary"):
    slide_outline = st.session_state['stage2_result']['slide_outline']
    total_slides = len(slide_outline)
    progress_bar = st.progress(0, text=f"콘텐츠 생성 대기 중... (0/{total_slides})")
    
    content_generator = ContentGenerator()
    generated_slides = {}

    for i, slide_info in enumerate(slide_outline):
        # 실시간 생성 과정 시뮬레이션
        time.sleep(0.5) # 실제 LLM 호출 시간 가정
        progress_text = f"콘텐츠 생성 중... ({i+1}/{total_slides}) - Slide {slide_info['slide_number']}"
        progress_bar.progress((i + 1) / total_slides, text=progress_text)
        
        # 가상 콘텐츠 생성
        slide_content = content_generator.generate_slide_content(slide_info)
        generated_slides[slide_info['slide_number']] = slide_content

    st.session_state['stage3_result'] = generated_slides
    progress_bar.empty() # 진행률 바 제거
    st.success("✅ 모든 슬라이드 콘텐츠 생성 완료!")

# 콘텐츠 생성 결과 표시 및 수정
if st.session_state['stage3_result']:
    st.markdown("--- ")
    st.subheader("생성된 슬라이드 콘텐츠 (수정 가능)")
    
    slide_results = st.session_state['stage3_result']
    for slide_num, slide_data in slide_results.items():
        with st.expander(f"**Slide {slide_num}:** {slide_data['headline']}"):
            editable_content = slide_data['content']
            
            # 헤드라인 수정
            slide_data['headline'] = st.text_input("헤드라인", value=slide_data['headline'], key=f"h_{slide_num}")
            
            # 인사이트 래더 시각화 및 수정
            st.markdown("**💡 인사이트 래더**")
            editable_content['insight_level_1'] = st.text_input("Level 1", value=editable_content['insight_level_1'], key=f"i1_{slide_num}")
            editable_content['insight_level_2'] = st.text_input("Level 2", value=editable_content['insight_level_2'], key=f"i2_{slide_num}")
            editable_content['insight_level_3'] = st.text_input("Level 3", value=editable_content['insight_level_3'], key=f"i3_{slide_num}")
            editable_content['insight_level_4'] = st.text_input("Level 4", value=editable_content['insight_level_4'], key=f"i4_{slide_num}")
            
            # 본문 및 액션 아이템 수정
            st.markdown("**📝 본문 및 액션 아이템**")
            body_text = "\n".join(editable_content['body_points'])
            edited_body = st.text_area("본문", value=body_text, key=f"b_{slide_num}", height=100)
            editable_content['body_points'] = edited_body.split('\n')
            
            action_text = "\n".join(editable_content['action_items'])
            edited_action = st.text_area("액션 아이템", value=action_text, key=f"a_{slide_num}", height=70)
            editable_content['action_items'] = edited_action.split('\n')

    # 다음 단계로 이동 버튼
    if st.button("→ Stage 4: 디자인 적용으로 이동", type="primary"):
        st.switch_page("pages/4_🎨_디자인적용.py")