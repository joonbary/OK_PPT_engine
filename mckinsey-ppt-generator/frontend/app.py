import streamlit as st

# 방어적 렌더링: 예외 발생 시 화면에 표시
try:
    st.set_page_config(
        page_title="McKinsey PPT Generator",
        page_icon="🧩",
        layout="wide",
    )

    st.title("McKinsey PPT Generator")
    st.caption("Health: UI loaded ✅")
    st.markdown("---")
    st.info("좌측 사이드바에서 단계를 선택해 PPT를 생성하세요.")

    st.subheader("진행 단계")
    st.markdown(
        """
        1. 문서 분석: 업로드/입력하면 LLM 분석으로 핵심 내용을 도출합니다.
        2. 구조 설계: MECE 원칙으로 스토리라인 구조를 설계합니다.
        3. 콘텐츠 생성: 스토리라인 기반 슬라이드/비주얼 콘텐츠를 만듭니다.
        4. 디자인 적용: 테마/레이아웃을 적용합니다.
        5. 품질 검토: So What, 논리성 등 품질을 점검합니다.
        """
    )

    with st.sidebar:
        st.title("도구")
        st.caption("Health: Sidebar loaded ✅")
        if st.checkbox("디버그 모드"):
            st.subheader("세션 상태")
            st.json(st.session_state)
except Exception as e:
    st.error("초기 렌더링 중 오류가 발생했습니다.")
    st.exception(e)

