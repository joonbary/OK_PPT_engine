import streamlit as st
import sys
import os
import io
import uuid
import requests
from docx import Document
import PyPDF2

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from frontend.components.progress_tracker import render_progress_tracker
except Exception:
    def render_progress_tracker(current_stage: int = 1):
        st.caption(f"Stage {current_stage} 진행 중")

API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

def parse_document(uploaded_file):
    file_type = uploaded_file.type
    text = f"'{uploaded_file.name}' 파일 내용입니다."
    try:
        if file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(io.BytesIO(uploaded_file.getvalue()))
            text = "\n".join([para.text for para in doc.paragraphs])
        elif file_type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            text = ""
            for page in pdf_reader.pages:
                try:
                    text += (page.extract_text() or "") + "\n"
                except Exception:
                    continue
        elif file_type == "text/plain":
            text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
        return text
    except Exception as e:
        st.error(f"파일 처리 오류 발생: {e}")
        return None

def analyze_via_api(document_text: str, language: str = 'ko'):
    url = f"{API_BASE_URL}/api/v1/analyze"
    payload = {
        "project_id": str(uuid.uuid4()),
        "document": document_text,
        "language": language or 'ko'
    }
    resp = requests.post(url, json=payload, timeout=(15, 240))
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict) and data.get('status') == 'completed':
        return data
    raise RuntimeError(data.get('error') or f"analyze_failed: {data}")

st.set_page_config(page_title="Stage 1: 문서 분석", page_icon="🧪", layout="wide")
st.title("Stage 1: 문서 분석")
render_progress_tracker(current_stage=1)

if 'stage1_result' not in st.session_state:
    st.session_state['stage1_result'] = None
if 'project_id' not in st.session_state:
    st.session_state['project_id'] = None
if 'document_text' not in st.session_state:
    st.session_state['document_text'] = None
if 'stage1_history' not in st.session_state:
    # Stack of snapshots: {result, project_id, document_text}
    st.session_state['stage1_history'] = []

col1, col2 = st.columns([2, 1])
with col1:
    uploaded_file = st.file_uploader(
        "분석할 비즈니스 문서를 업로드하세요.",
        type=['docx', 'pdf', 'txt'],
        help="지원 형식: DOCX, PDF, TXT (최대 10MB)"
    )
    text_input = st.text_area(
        "또는 분석할 텍스트를 직접 입력하세요.",
        height=250,
        placeholder="예) '이번 분기 매출은 20% 성장했으며...'"
    )

if st.button("🧠 분석 시작", type="primary"):
    if uploaded_file or text_input:
        with st.spinner("AI가 문서를 분석하고 있습니다. 잠시만 기다려 주세요..."):
            content_to_analyze = ""
            if uploaded_file:
                if uploaded_file.size > 10 * 1024 * 1024:
                    st.error("파일 크기가 10MB를 초과합니다. 더 작은 파일로 업로드해 주세요.")
                    st.stop()
                content_to_analyze = parse_document(uploaded_file)
            else:
                content_to_analyze = text_input

            if content_to_analyze:
                try:
                    analysis = analyze_via_api(content_to_analyze, 'ko')
                    # push previous snapshot for rollback
                    st.session_state['stage1_history'].append({
                        'result': st.session_state.get('stage1_result'),
                        'project_id': st.session_state.get('project_id'),
                        'document_text': st.session_state.get('document_text'),
                    })
                    st.session_state['stage1_result'] = analysis.get('result', {})
                    st.session_state['project_id'] = analysis.get('project_id')
                    st.session_state['document_text'] = content_to_analyze
                    st.success("문서 분석 완료!")
                except Exception as e:
                    st.error(f"분석 실패: {e}")
    else:
        st.error("파일을 업로드하거나 텍스트를 입력해야 합니다.")

if st.session_state['stage1_result']:
    st.markdown("--- ")
    st.subheader("AI 분석 결과")
    result = st.session_state['stage1_result']

    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric(label="핵심 메시지", value=result.get('core_message', '-') or result.get('key_message', '-'))
        st.text(" ")
        st.subheader("상위 주요 토픽")
        topics = result.get('key_topics', []) or ['-']
        for topic in topics:
            st.markdown(f"- {topic}")

    with res_col2:
        st.metric(label="타겟 오디언스", value=result.get('target_audience', '-'))
        st.text(" ")
        st.subheader("주요 데이터 포인트")
        dps = result.get('data_points', [])
        if dps and all(isinstance(x, str) for x in dps):
            dps = [{"type": "Insight", "value": x, "context": ""} for x in dps[:20]]
        st.dataframe(dps)

    cols = st.columns([1,1,2])
    with cols[0]:
        if st.session_state['stage1_history']:
            if st.button("↩ 이전 결과로 롤백"):
                snap = st.session_state['stage1_history'].pop()
                st.session_state['stage1_result'] = snap.get('result')
                st.session_state['project_id'] = snap.get('project_id')
                st.session_state['document_text'] = snap.get('document_text')
                st.toast("이전 분석 결과로 롤백했습니다.")
                st.experimental_rerun()
    with cols[2]:
        if st.button("➡️ Stage 2로 이동", type="primary"):
            try:
                st.switch_page("pages/2_structure.py")
            except Exception:
                pass
