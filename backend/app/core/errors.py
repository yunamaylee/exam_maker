from typing import Optional, Any, Literal, NoReturn

ErrorSource = Literal["repository", "service"]

ERROR_DISPLAY_MESSAGES: dict[str, str] = {
    "NOT_FOUND": "요청한 리소스를 찾을 수 없습니다.",
    "UNAUTHORIZED": "인증이 필요합니다.",
    "FORBIDDEN": "접근 권한이 없습니다.",
    "VALIDATION_ERROR": "입력값이 올바르지 않습니다.",
    "INTERNAL_ERROR": "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
    "DUPLICATE": "이미 존재하는 데이터입니다.",
    "DB_CONNECTION_ERROR": "데이터베이스 연결 오류가 발생했습니다.",
    "DATA_ERROR": "잘못된 데이터 형식입니다.",
}

DEFAULT_DISPLAY_MESSAGE = "알 수 없는 오류가 발생했습니다."


class AppError(Exception):
    def __init__(
        self,
        source: ErrorSource,
        code: str,
        message: str,
        cause: Optional[Exception] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.source = source
        self.code = code
        self.message = message
        self.cause = cause
        self.context = context or {}

    def __repr__(self) -> str:
        return (
            f"AppError(source={self.source!r}, code={self.code!r}, "
            f"message={self.message!r}, context={self.context!r})"
        )


def create_repo_error(
    code: str,
    message: str,
    cause: Optional[Exception] = None,
    context: Optional[dict[str, Any]] = None,
) -> AppError:
    return AppError(
        source="repository",
        code=code,
        message=message,
        cause=cause,
        context=context,
    )


def handle_service_error(
    error: Exception,
    code: str = "INTERNAL_ERROR",
    message: str = "서비스 처리 중 오류가 발생했습니다.",
    context: Optional[dict[str, Any]] = None,
) -> NoReturn:
    if isinstance(error, AppError):
        raise error

    raise AppError(
        source="service",
        code=code,
        message=message,
        cause=error,
        context=context,
    )


def get_display_message(code: str) -> str:
    # 슬래시 계층형 코드에서 마지막 세그먼트 추출
    # 예: "REPO/EXAM/NOT_FOUND" → "NOT_FOUND"
    last_segment = code.split("/")[-1]
    return ERROR_DISPLAY_MESSAGES.get(last_segment, DEFAULT_DISPLAY_MESSAGE)


def map_sqlalchemy_error(
    error: Exception,
    code: str,
    context: Optional[dict[str, Any]] = None,
) -> AppError:
    from sqlalchemy.exc import IntegrityError, OperationalError, DataError
    if isinstance(error, IntegrityError):
        return AppError(
            source="repository",
            code="REPO/DUPLICATE",
            message="중복된 데이터입니다.",
            cause=error,
            context=context,
        )
    elif isinstance(error, OperationalError):
        return AppError(
            source="repository",
            code="REPO/DB_CONNECTION_ERROR",
            message="데이터베이스 연결 오류가 발생했습니다.",
            cause=error,
            context=context,
        )
    elif isinstance(error, DataError):
        return AppError(
            source="repository",
            code="REPO/DATA_ERROR",
            message="잘못된 데이터 형식입니다.",
            cause=error,
            context=context,
        )
    else:
        return AppError(
            source="repository",
            code=code,
            message=str(error),
            cause=error,
            context=context,
        )