from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services import exam as exam_service
from app.schemas.exam import GenerateExamRequest

router = APIRouter(prefix="/api/v1/exam", tags=["exam"])

# 시험 패턴 분석 함수
@router.post("/analyze")
async def analyze_exam(
    school_name: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # PDF 바이트로 읽기
    pdf_bytes = await file.read()
    
    # 텍스트 추출
    pdf_text = exam_service.extract_pdf_text(pdf_bytes)
    
    # 패턴 분석
    analysis = exam_service.analyze_exam_pattern(
        db=db,
        school_name=school_name,
        pdf_text=pdf_text,
    )
    
    return {
        "success": True,
        "analysis_id": str(analysis.id),
        "message": "기출 분석이 완료됐습니다.",
    }


# 시험 범위 본문 추출 함수
@router.post("/range")
async def extract_exam_range(
    file: UploadFile = File(...),
):
    # PDF 바이트로 읽기
    pdf_bytes = await file.read()
    
    # 텍스트 추출
    pdf_text = exam_service.extract_pdf_text(pdf_bytes)
    
    # 본문 추출
    passages = exam_service.extract_passages(pdf_text)
    
    return {
        "success": True,
        "passages": passages,
    }

# 시험지 생성 함수
@router.post("/generate")
async def generate_exam(
    analysis_id: str,
    request: GenerateExamRequest,
    db: Session = Depends(get_db),
):
    exam = exam_service.generate_exam(
        db=db,
        analysis_id=analysis_id,
        passages=request.passages.dict(),
        options=request.options.dict(),
    )
    
    return {
        "success": True,
        "exam_id": str(exam.id),
        "exam": exam.exam_content,
    }