"""
PptxGenerator 테스트
"""

import pytest
from unittest.mock import MagicMock, patch
from app.services.pptx_generator import PptxGenerator

@pytest.fixture
def mock_ppt_data():
    return {
        'slides': [
            {
                'slide_number': 1,
                'layout_suggestion': 'title_slide',
                'title': 'Test Presentation',
                'key_points': []
            },
            {
                'slide_number': 2,
                'layout_suggestion': 'title_and_content',
                'title': 'Test Slide 2',
                'key_points': ['Point 1', 'Point 2'],
                'content_type': 'text'
            }
        ],
        'job_id': 'test_job'
    }

def test_pptx_generator_initialization():
    """PptxGenerator 초기화 테스트"""
    generator = PptxGenerator()
    assert generator is not None

@patch('app.services.pptx_generator.Presentation')
@patch('app.services.pptx_generator.ChartGenerator')
@patch('app.services.pptx_generator.FileManager')
def test_generate_pptx(MockFileManager, MockChartGenerator, MockPresentation, mock_ppt_data):
    """PPTX 생성 테스트"""
    # Mock FileManager
    mock_file_manager = MockFileManager.return_value
    mock_file_manager.save_file.return_value = "/tmp/test.pptx"

    # Mock Presentation
    mock_prs = MockPresentation.return_value
    mock_prs.slides.add_slide.return_value = MagicMock()

    generator = PptxGenerator()
    file_path = generator.generate(mock_ppt_data)

    assert file_path == "/tmp/test.pptx"
    # Presentation이 한번 호출되었는지 확인
    MockPresentation.assert_called_once()
    # slides.add_slide가 slide 수만큼 호출되었는지 확인
    assert mock_prs.slides.add_slide.call_count == len(mock_ppt_data['slides'])
    # save가 한번 호출되었는지 확인
    mock_prs.save.assert_called_once()
    # file_manager.save_file이 한번 호출되었는지 확인
    mock_file_manager.save_file.assert_called_once()
