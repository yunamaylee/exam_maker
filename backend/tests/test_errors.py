import pytest
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
    message = get_display_message("UNKNOWN/CODE")
    assert message == "알 수 없는 오류가 발생했습니다."


# handle_service_error AppError 재랩핑 방지 테스트
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
    assert error.code == "REPO/EXAM/GET_ANALYSIS"
    assert error.source == "repository"