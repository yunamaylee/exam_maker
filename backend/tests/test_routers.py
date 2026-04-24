import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.models.exam import ExamAnalysis, ExamResult
from app.dependencies import get_db


# DB 의존성 모킹
@pytest.fixture
def mock_db():
    db = MagicMock()
    app.dependency_overrides[get_db] = lambda: db
    yield db
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


# 헬스체크 테스트
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# 시험 패턴 분석 테스트
def test_analyze_exam_success(client, mock_db):
    mock_analysis = ExamAnalysis(
        id=uuid.uuid4(),
        school_name="테스트고등학교",
        analysis_result={"pattern": "test"},
    )

    with patch(
        "app.services.exam.analyze_exam_from_pdf",
        new_callable=AsyncMock,
        return_value=mock_analysis,
    ):
        pdf_content = b"%PDF-1.4 test content"
        response = client.post(
            "/api/v1/exam/analyze?school_name=테스트고등학교",
            files={"file": ("test.pdf", pdf_content, "application/pdf")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "기출 분석이 완료됐습니다."
    assert "analysis_id" in data


# 시험 패턴 분석 실패 테스트 (AppError)
def test_analyze_exam_app_error(client, mock_db):
    from app.core.errors import AppError

    with patch(
        "app.services.exam.analyze_exam_from_pdf",
        new_callable=AsyncMock,
        side_effect=AppError(
            source="service",
            code="SERVICE/EXAM/ANALYZE_FROM_PDF",
            message="PDF 분석 중 오류가 발생했습니다.",
        ),
    ):
        pdf_content = b"%PDF-1.4 test content"
        response = client.post(
            "/api/v1/exam/analyze?school_name=테스트고등학교",
            files={"file": ("test.pdf", pdf_content, "application/pdf")},
        )

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "code" in data


# 시험지 생성 테스트
def test_generate_exam_success(client, mock_db):
    mock_exam = ExamResult(
        id=uuid.uuid4(),
        analysis_id=uuid.uuid4(),
        exam_content={"questions": []},
    )

    with patch(
        "app.services.exam.generate_exam",
        new_callable=AsyncMock,
        return_value=mock_exam,
    ):
        response = client.post(
            f"/api/v1/exam/generate?analysis_id={uuid.uuid4()}",
            json={
                "passages": {"text": "test passage"},
                "options": {"count": 5},
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "exam_id" in data


# 시험지 조회 - 존재하지 않는 경우 테스트
def test_download_exam_not_found(client, mock_db):
    from app.core.errors import AppError

    with patch(
        "app.services.exam.get_exam",
        new_callable=AsyncMock,
        side_effect=AppError(
            source="repository",
            code="REPO/EXAM/RESULT_NOT_FOUND",
            message="시험지를 찾을 수 없습니다.",
        ),
    ):
        response = client.get(f"/api/v1/exam/{uuid.uuid4()}/download")

    assert response.status_code == 404