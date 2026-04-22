from fastapi import FastAPI, Request
from app.routers import exam as exam_router
from app.core.errors import AppError, get_display_message
from fastapi.responses import JSONResponse


app = FastAPI(title="exam_maker")
app.include_router(exam_router.router)

#에러 핸들러
@app.exception_handler(AppError)
async def app_error_handler(request: Request, error: AppError):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message" : get_display_message(error.code),
            "code": error.code,
            "source": error.source,
        }
    )

@app.on_event("startup")
async def startup():
    print("exam_maker 서버 시작!")