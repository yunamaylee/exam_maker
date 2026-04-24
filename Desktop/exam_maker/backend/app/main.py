from fastapi import FastAPI, Request
from app.routers import exam as exam_router
from app.core.errors import AppError, get_display_message
from app.core.config import ALLOWED_ORIGINS
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="exam_maker")

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
    "FORBIDDEN": 403,
    "VALIDATION_ERROR": 422,
    "DUPLICATE": 409,
    "INTERNAL_ERROR": 500,
    "DB_CONNECTION": 503,
    "DB_TIMEOUT": 503,
    "DB_INVALID_DATA": 400,
}

def get_http_status(code: str) -> int:
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

@app.on_event("startup")
async def startup():
    print("exam_maker 서버 시작!")