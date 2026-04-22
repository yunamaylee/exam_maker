from typing import Optional, Any, Literal

ErrorSource = Literal["repository", "service"]

ERROR_DISPLAY_MESSAGES: dict[str, str] = {
    "NOT_FOUND": "요청한 리소스를 찾을 수 없습니다.",
    "UNAUTHORIZED": "인증이 필요합니다.",
    "FORBIDDEN": "접근 권한이 없습니다.",
    "VALIDATION_ERROR": "입력값이 올바르지 않습니다.",
    "INTERNAL_ERROR": "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
    "DUPLICATE": "이미 존재하는 데이터입니다.",
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
) -> None:
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
    return ERROR_DISPLAY_MESSAGES.get(code, DEFAULT_DISPLAY_MESSAGE)