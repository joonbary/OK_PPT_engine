# D:\PPT_Designer_OK\mckinsey-ppt-generator\frontend\pages\5_✅_품질검토.py

import streamlit as st
import sys
import os
import plotly.graph_objects as go
import pandas as pd

# 프로젝트 루트 경로 설정
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from frontend.components.progress_tracker import render_progress_tracker

# --- Mock/Placeholder Implementations ---
class QualityController:
    """PPT 품질을 검토하고 점수를 매기는 가상 Controller"""
    def run_quality_check(self, pptx_path):
        # stage5.txt의 JSON 구조에 따라 모의 데이터를 생성합니다.
        return {
            "total_score": 0.873,
            "passed": True,
            "scores": {
                "Clarity": 0.93,
                "Insight": 0.80,
                "Structure": 0.72,
                "Visual": 0.95,
                "Actionability": 1.00
            },
            "improvements": [
                {"area": "Structure", "issue": "슬라이드 7-9의 논리적 연결 미흡", "suggestion": "전환 슬라이드 추가 권장"}
            ],
            "iteration_history": [
                {"iteration": 1, "score": 0.665},
                {"iteration": 2, "score": 0.821},
                {"iteration": 3, "score": 0.873}
            ]
        }

# --- Streamlit UI ---
st.set_page_config(page_title="Stage 5: 품질 검토", page_icon="✅", layout="wide")

st.title("✅ Stage 5: 품질 검토")
render_progress_tracker(current_stage=5)

# Stage 4 결과 확인
if 'stage4_result' not in st.session_state or st.session_state['stage4_result'] is None:
    st.warning("⚠️ Stage 4: 디자인 적용을 먼저 완료해주세요.")
    st.page_link("pages/4_🎨_디자인적용.py", label="Stage 4로 이동")
    st.stop()

# 세션 상태 초기화
if 'stage5_result' not in st.session_state:
    st.session_state['stage5_result'] = None

# 품질 검토 버튼
st.info("완성된 PPT를 최종 검토하고, McKinsey 품질 기준에 따라 점수를 매깁니다.")
if st.button("✅ 품질 검토 시작", type="primary"):
    with st.spinner("AI가 최종 품질을 검토 중입니다..."):
        controller = QualityController()
        pptx_path = st.session_state['stage4_result']['output_pptx_path']
        quality_result = controller.run_quality_check(pptx_path)
        st.session_state['stage5_result'] = quality_result
    st.success("✅ 품질 검토 완료!")

# 품질 검토 결과 표시
if st.session_state['stage5_result']:
    st.markdown("--- ")
    st.subheader("최종 품질 검토 보고서")
    result = st.session_state['stage5_result']
    
    # 최종 점수
    score_color = "blue" if result['passed'] else "red"
    st.markdown(f"### 🏆 최종 품질 점수: <span style='color:{score_color}; font-size: 1.5em;'>{result['total_score']:.3f}</span> / 1.000", unsafe_allow_html=True)
    if result['passed']:
        st.success("✅ 목표 품질 점수(0.85)를 달성했습니다!")
    else:
        st.error("❌ 목표 품질 점수에 미달했습니다. 개선 제안을 확인하세요.")

    col1, col2 = st.columns([3, 2])
    with col1:
        # 레이더 차트 시각화
        st.subheader("📊 5대 품질 지표")
        categories = list(result['scores'].keys())
        scores = list(result['scores'].values())
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='품질 점수'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # 개선 제안 및 이력
        st.subheader("💡 개선 제안")
        for imp in result['improvements']:
            st.warning(f"**[{imp['area']}]** {imp['issue']} → **{imp['suggestion']}**")
        
        st.subheader("🔄 반복 개선 이력")
        history_df = pd.DataFrame(result['iteration_history'])
        st.line_chart(history_df.set_index('iteration'))

    # 다운로드 버튼
    st.markdown("--- ")
    st.subheader("🎉 최종 산출물 다운로드")
    pptx_path = st.session_state['stage4_result']['output_pptx_path']
    with open(pptx_path, "rb") as f:
        st.download_button(
            label="📥 PPTX 파일 다운로드",
            data=f,
            file_name="generated_presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
