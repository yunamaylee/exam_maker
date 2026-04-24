import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from app.routers import exam as exam_router
from app.core.errors import AppError, get_display_message
from app.core.config import ALLOWED_ORIGINS
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시
    logger.info("exam_maker 서버 시작!")
    yield
    # 서버 종료 시
    logger.info("exam_maker 서버 종료!")


app = FastAPI(title="exam_maker", lifespan=lifespan)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(exam_router.router)

# 에러 코드 → HTTP status code 매핑
ERROR_STATUS_MAP: dict[str, int] = {
    "NOT_FOUND": 404,
    "UNAUTHORIZED": 401,
    "FORBTE": 409,
    "INTERNAL_ERROR": 500,
    "DB_CONNECTION_ERROR": 503,
    "DATA_ERROR": 400,
}


def get_http_status(code: str) -> int:
    # 슬래시 계층형 코드에서 마지막 세그먼트 추출
    # 예: "REPO/EXAM/NOT_FOUND" → "NOT_FOUND" → 404
    last_segment = code.split("/")[-1]
    return ERROR_STATUS_MAP.get(last_segment, 400)


# 에러 핸들러
@app.exception_handler(AppError)
async def app_error_handler(request: Request, error: AppError):
    return JSONResponse(
        status_code=get_http_status(error.code),
        content={
            "success": False,
            "message": get_display_message(error.code),
            "code": error.code,
            "source": error.source,
        }
    )


# 헬스체크
@app.get("/health")
async def health_check():
    return {"status": "ok"}
