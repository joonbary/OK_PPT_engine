"""
AI Content to PPT Integration Fix
문제: AI가 생성한 콘텐츠가 실제 PPT에 반영되지 않음
해결: PPTGenerator에 generate() 메서드 추가
"""

# app/services/ppt_generator.py에 추가할 메서드

async def generate(self, result: Dict) -> Presentation:
    """
    AI 워크플로우 결과를 실제 PPT로 변환
    
    Args:
        result: WorkflowOrchestrator의 결과
            {
                "slides": [
                    {
                        "type": "title",
                        "headline": "AI 생성 헤드라인", 
                        "subtitle": "부제목",
                        "content": ["포인트1", "포인트2"],
                        "chart": {...}
                    },
                    ...
                ],
                "quality_score": 0.85
            }
    
    Returns:
        Presentation: 생성된 PPT 객체
    """
    logger.info("🎨 Generating PPT from AI result...")
    
    prs = Presentation()
    
    # AI 결과에서 슬라이드 데이터 추출
    slides_data = result.get("slides", [])
    
    if not slides_data:
        logger.warning("⚠️ No slides data in result, generating fallback")
        return self._generate_fallback_ppt()
    
    logger.info(f"📊 Creating {len(slides_data)} slides from AI content")
    
    # McKinsey 색상 정의
    mckinsey_blue = RGBColor(0, 118, 168)  # #0076A8
    text_gray = RGBColor(83, 86, 90)       # #53565A
    
    # 각 슬라이드를 AI 데이터로 생성
    for idx, slide_data in enumerate(slides_data, 1):
        try:
            slide_type = slide_data.get("type", "content")
            logger.info(f"  Creating slide {idx}/{len(slides_data)}: {slide_type}")
            
            # 슬라이드 타입에 따른 레이아웃 선택
            if slide_type == "title":
                layout = prs.slide_layouts[0]  # Title Slide
            else:
                layout = prs.slide_layouts[1]  # Title and Content
            
            slide = prs.slides.add_slide(layout)
            
            # AI 생성 헤드라인 적용 (핵심!)
            if slide.shapes.title:
                headline = slide_data.get("headline", "")
                slide.shapes.title.text = headline
                logger.info(f"    ✨ AI Headline: {headline}")
                
                # McKinsey 스타일 적용
                title_frame = slide.shapes.title.text_frame
                for paragraph in title_frame.paragraphs:
                    paragraph.font.size = Pt(18)
                    paragraph.font.bold = True
                    paragraph.font.color.rgb = mckinsey_blue
            
            # 부제목 (표지 슬라이드용)
            if slide_type == "title" and len(slide.shapes) > 1:
                subtitle = slide_data.get("subtitle", "")
                slide.shapes[1].text = subtitle
            
            # AI 생성 콘텐츠 적용
            content_list = slide_data.get("content", [])
            if content_list and len(slide.shapes) > 1:
                # Content placeholder 찾기
                for shape in slide.shapes:
                    if shape.has_text_frame and shape != slide.shapes.title:
                        text_frame = shape.text_frame
                        text_frame.clear()
                        
                        for item in content_list:
                            p = text_frame.add_paragraph()
                            p.text = item
                            p.level = 0
                            p.font.size = Pt(14)
                            p.font.color.rgb = text_gray
                            p.space_after = Pt(12)
                        break
            
        except Exception as e:
            logger.error(f"  ❌ Failed to create slide {idx}: {e}")
            # 실패해도 계속 진행
    
    logger.info(f"✅ PPT generation complete: {len(prs.slides)} slides")
    return prs

def _generate_fallback_ppt(self) -> Presentation:
    """긴급 폴백 (AI 데이터 없을 때만)"""
    logger.warning("🚨 Generating emergency fallback PPT")
    prs = Presentation()
    
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Error: No AI Content"
    
    return prs


# 추가로 수정이 필요한 부분:
# app/services/workflow_orchestrator.py의 execute() 메서드가
# AI 생성 결과를 올바른 구조로 반환하는지 확인 필요

"""
수정 방법:
1. 위의 generate() 메서드를 PPTGenerator 클래스에 추가
2. PPT 생성 시 이 메서드를 호출하도록 변경
3. AI 워크플로우 결과가 올바른 구조인지 확인
"""