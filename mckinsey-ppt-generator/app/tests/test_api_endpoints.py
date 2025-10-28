"""
API 엔드포인트 테스트
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_redis():
    with patch('app.api.ppt_endpoints.RedisClient') as mock:
        instance = mock.return_value
        instance.set_ppt_status = AsyncMock()
        instance.get_ppt_status = AsyncMock()
        yield instance

@pytest.fixture
def mock_background_tasks():
    with patch('app.api.ppt_endpoints.BackgroundTasks') as mock:
        yield mock

def test_health_check():
    """헬스 체크 테스트"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_generate_ppt(mock_redis, mock_background_tasks):
    """PPT 생성 요청 테스트"""
    # BackgroundTasks.add_task를 모의 처리합니다.
    with patch('fastapi.BackgroundTasks.add_task') as mock_add_task:
        response = client.post(
            "/api/v1/generate-ppt",
            json={
                "document": "테스트 문서입니다. " * 20,  # 최소 길이 충족
                "style": "mckinsey",
                "num_slides": 10,
                "language": "ko",
                "target_audience": "executive"
            }
        )
        assert response.status_code == 202
        data = response.json()
        assert "ppt_id" in data
        assert data["status"] == "processing"
        # Redis에 상태가 저장되었는지 확인
        mock_redis.set_ppt_status.assert_called_once()
        # 백그라운드 작업이 추가되었는지 확인
        mock_add_task.assert_called_once()

def test_get_ppt_status_not_found(mock_redis):
    """존재하지 않는 PPT 조회 테스트"""
    mock_redis.get_ppt_status.return_value = None
    response = client.get("/api/v1/ppt-status/invalid-id")
    assert response.status_code == 404