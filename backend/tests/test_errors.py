import pytest
from unittest.mock import MagicMock, patch
from app.core.errors import (
    AppError,
    create_repo_error,
    handle_service_error,
    get_display_message,
    map_sqlalchemy_error,
)
from sqlalchemy.exc import IntegrityError, OperationalError, DataError


# AppError 생성 테스트
def test_create_repo_error():
    error = create_repo_error(
        code="REPO/EXAM/NOT_FOUND",
        message="분석 결과를 찾을 수 없습니다.",
    )
    assert error.source == "repository"
    assert error.code == "REPO/EXAM/NOT_FOUND"
    assert error.message == "분석 결과를 찾을 수 없습니다."


# get_display_message 슬래시 계층형 코드 테스트
def test_get_display_message_with_slash_code():
    message = get_display_message("REPO/EXAM/NOT_FOUND")
    assert message == "요청한 리소스를 찾을 수 없습니다."


# get_display_message 알 수 없는 코드 테스트
def test_get_display_message_unknown_code():
    me지 테스트
def test_handle_service_error_no_rewrap():
    original = AppError(
        source="repository",
        code="REPO/EXAM/NOT_FOUND",
        message="분석 결과를 찾을 수 없습니다.",
    )
    with pytest.raises(AppError) as exc_info:
        handle_service_error(original, code="SERVICE/EXAM/ANALYZE_PATTERN")
    # 재랩핑 없이 원본 AppError 그대로 올라와야 함
    assert exc_info.value.code == "REPO/EXAM/NOT_FOUND"
    assert exc_info.value.source == "repository"


# map_sqlalchemy_error IntegrityError 테스트
def test_map_sqlalchemy_error_integrity():
    error = map_sqlalchemy_error(
        IntegrityError("duplicate", {}, None),
        code="REPO/EXAM/SAVE_ANALYSIS",
    )
    assert error.code == "REPO/DUPLICATE"
    assert error.source == "repository"


# map_sqlalchemy_error 기본 케이스 테스트
def test_map_sqlalchemy_error_default():
    error = map_sqlalchemy_error(
        Exception("unknown error"),
        code="REPO/EXAM/GET_ANALYSIS",
    )
    a


# 서비스 레이어 - 캐싱 동작 테스트
def test_analyze_exam_pattern_returns_cached_result():
    from app.services.exam import analyze_exam_pattern
    from app.models.exam import ExamAnalysis
    import uuid

    mock_db = MagicMock()
    mock_analysis = ExamAnalysis(
        id=uuid.uuid4(),
        school_name="테스트고등학교",
        analysis_result={"pattern": "test"},
    )

    with patch(
        "app.repositories.exam.get_analysis_by_school_name",
        return_value=mock_analysis,
    ):
        result = analyze_exam_pattern(
            db=mock_db,
            school_name="테스트고등학교",
            pdf_text="시험 내용",
        )
        assert result == mock_analysis


# 서비스 레이어 - 빈 PDF 텍스트 예외 테스트
def test_analyze_exam_pattern_raises_on_empty_pdf():
    from app.services.exam import analyze_exam_pattern

    mock_db = MagicMock()

    with patch(
        "app.repositories.exam.get_analysis_by_school_name",
        return_value=Non(
                db=mock_db,
                school_name="테스트고등학교",
                pdf_text="",
            )
        assert exc_info.value.source == "service"
