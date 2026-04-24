import io
from typing import List
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services import exam as exam_service
from app.services.docx import create_exam_docx
from app.schemas.exam import GenerateExamRequest

router = APIRouter(prefix="/api/v1/exam", tags=["exam"])


# 시험 패턴 분석
@router.post("/analyze")
async def analyze_exam(
    school_name: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    pdf_bytes = await file.read()
    # 라우터는 서비스만 호출 — PDF 추출은 서비스 내부에서 처리
    analysis = exam_service.analyze_exam_from_pdf(
        db=db,
        school_name=school_name,
        pdf_bytes=pdf_bytes,
    )
    return {
        "success": True,
        "analysis_id": str(analysis.id),
        "analysis_result": analysis.analysis_result,
        .post("/range")
async def extract_exam_range(
    files: List[UploadFile] = File(...),
):
    all_passages = {}
    for file in files:
        pdf_bytes = await file.read()
        # 라우터는 서비스만 호출 — PDF 추출은 서비스 내부에서 처리
        passages = exam_service.extract_passages_from_pdf(pdf_bytes=pdf_bytes)
        all_passages.update(passages)
    return {
        "success": True,
        "passages": all_passages,
    }


# 시험지 생성
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


# 시험지 docx 다운로드
@router.get("/{exam_id}/download")
async def download_exam(
    exam_id: str,
(
        db=db,
        exam_id=exam_id,
    )
    docx_bytes = create_exam_docx(exam.exam_content)
    return StreamingResponse(
        io.BytesIO(docx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=exam_{exam_id}.docx"}
    )
