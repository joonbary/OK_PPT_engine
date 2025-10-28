import streamlit as st
import sys
import os
import requests

# project root onto sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from frontend.components.progress_tracker import render_progress_tracker

API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')


def structure_via_api(project_id: str, document_text: str, num_slides: int, language: str = 'ko'):
    url = f"{API_BASE_URL}/api/v1/structure"
    payload = {
        "project_id": project_id,
        "document": document_text,
        "num_slides": num_slides,
        "language": language or 'ko'
    }
    resp = requests.post(url, json=payload, timeout=(15, 240))
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict) and data.get('status') == 'completed':
        return data.get('result', {})
    raise RuntimeError(data.get('error') or f"structure_failed: {data}")


st.set_page_config(page_title="Stage 2: 구조 설계", page_icon="🧱", layout="wide")
st.title("Stage 2: 구조 설계")
render_progress_tracker(current_stage=2)

# Stage 1 선행 확인 및 입력 준비
if not st.session_state.get('stage1_result'):
    st.warning("⚠️ 먼저 Stage 1: 문서 분석을 완료해 주세요.")
    try:
        st.page_link("pages/1_📄_문서분석.py", label="Stage 1로 이동")
    except Exception:
        pass
    st.stop()

if not st.session_state.get('document_text'):
    st.error("원본 문서 텍스트가 없습니다. Stage 1을 다시 실행해 주세요.")
    st.stop()

if 'stage2_result' not in st.session_state:
    st.session_state['stage2_result'] = None

st.subheader("구조 설계 옵션")
col1, col2 = st.columns(2)
with col1:
    framework_hint = st.selectbox(
        "설계 힌트(참고)", ["자동", "3C", "4P", "SWOT", "Porter's 5 Forces", "기타"], index=0,
        help="현재 단계에서는 백엔드 에이전트가 적절한 프레임워크를 자동 선택합니다."
    )
with col2:
    num_slides = st.slider("목표 슬라이드 수", min_value=5, max_value=30, value=12)

if st.button("🧭 구조 설계 실행", type="primary"):
    with st.spinner("AI가 프레임워크/피라미드/아웃라인을 설계 중입니다..."):
        try:
            result = structure_via_api(
                st.session_state.get('project_id') or '',
                st.session_state['document_text'],
                num_slides,
                'ko'
            )
            st.session_state['stage2_result'] = result
            st.success("구조 설계 완료!")
        except requests.Timeout:
            st.error("요청 시간이 초과되었습니다. 다시 시도해 주세요.")
        except Exception as e:
            st.error(f"구조 설계 실패: {e}")


if st.session_state['stage2_result']:
    st.markdown("---")
    st.subheader("설계 결과 요약")
    res = st.session_state['stage2_result']
    mece = res.get('mece_segments') or []
    outline = res.get('slide_outline') or []

    st.caption(f"MECE 세그먼트: {len(mece)}개 | 슬라이드 아웃라인: {len(outline)}개")

    if mece:
        with st.expander("MECE 세그먼트 보기", expanded=False):
            for seg in mece:
                st.markdown(f"- [{seg.get('category','-')}] {seg.get('content','')[:120]}...")

    st.subheader("슬라이드 아웃라인")
    for i, slide in enumerate(outline):
        with st.expander(f"Slide {slide.get('slide_number', i+1)}: {slide.get('type','-')} — {slide.get('content_focus') or slide.get('headline','')}"):
            new_headline = st.text_input("헤드라인 수정", value=slide.get('headline') or slide.get('content_focus',''), key=f"headline_{i}")
            slide['headline'] = new_headline

    if st.button("➡️ Stage 3: 콘텐츠 생성으로 이동", type="primary"):
        try:
            st.switch_page("pages/3_✍️_콘텐츠생성.py")
        except Exception:
            pass

