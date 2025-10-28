import streamlit as st

st.set_page_config(
    page_title="McKinsey PPT Generator",
    page_icon="📄",
    layout="wide",
)

st.title("McKinsey PPT Generator")
st.markdown("---")
st.info("좌측 사이드바에서 단계를 선택해 PPT를 생성하세요.")

st.subheader("진행 단계")
st.markdown(
    """
    1. 문서 분석: 비즈니스 문서를 업로드/입력하면 LLM이 핵심 메시지와 주요 토픽을 추출합니다.
    2. 구조 설계: MECE 프레임으로 슬라이드 구조를 설계합니다.
    3. 콘텐츠 생성: 슬라이드 초안과 본문/하이라이트를 생성합니다.
    4. 디자인 적용: 스타일/레이아웃을 적용합니다.
    5. 품질 검토: So What, 명료성 등을 점검합니다.
    """
)

with st.sidebar:
    st.title("도구")
    if st.checkbox("디버그 모드"):
        st.subheader("세션 상태")
        st.json(st.session_state)
