# D:\PPT_Designer_OK\mckinsey-ppt-generator\frontend\components\progress_tracker.py

import streamlit as st

def render_progress_tracker(current_stage: int):
    """5단계 워크플로우의 현재 진행 상태를 시각적으로 표시하는 컴포넌트"""
    stages = [
        {"num": 1, "name": "문서분석", "icon": "📄"},
        {"num": 2, "name": "구조설계", "icon": "🏗️"},
        {"num": 3, "name": "콘텐츠생성", "icon": "✍️"},
        {"num": 4, "name": "디자인적용", "icon": "🎨"},
        {"num": 5, "name": "품질검토", "icon": "✅"}
    ]
    
    # 단계별 아이콘 및 캡션 표시
    cols = st.columns(len(stages))
    for i, stage in enumerate(stages):
        with cols[i]:
            if stage['num'] < current_stage:
                st.markdown(f"<div style='text-align: center; color: green;'>✅<br>{stage['name']}</div>", unsafe_allow_html=True)
            elif stage['num'] == current_stage:
                st.markdown(f"<div style='text-align: center; font-weight: bold;'>🔄<br>{stage['name']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: center; color: grey;'>⏳<br>{stage['name']}</div>", unsafe_allow_html=True)

    # 전체 진행률 바
    progress_percent = (current_stage - 1) / (len(stages) - 1) if len(stages) > 1 else 0
    st.progress(progress_percent)
    st.markdown("<hr>", unsafe_allow_html=True)
