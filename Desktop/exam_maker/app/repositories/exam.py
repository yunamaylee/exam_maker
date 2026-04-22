from sqlalchemy.orm import Session
from app.models.exam import ExamAnalysis, ExamResult
from app.core.errors import create_repo_error

def save_analysis(
    db: Session,
    school_name: str,
    analysis_result: dict,
) -> ExamAnalysis:
    try:
        analysis = ExamAnalysis(
            school_name=school_name,
            analysis_result=analysis_result,
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis
    except Exception as e:
        db.rollback()
        raise create_repo_error(
            code="REPO/EXAM/SAVE_ANALYSIS",
            message="분석 결과 저장 중 오류가 발생했습니다.",
            cause=e,
        )

def get_analysis(
    db: Session,
    analysis_id: str,
) -> ExamAnalysis:
    try:
        analysis = db.query(ExamAnalysis).filter(
            ExamAnalysis.id == analysis_id
        ).first()
        if not analysis:
            raise create_repo_error(
                code="REPO/EXAM/NOT_FOUND",
                message="분석 결과를 찾을 수 없습니다.",
            )
        return analysis
    except Exception as e:
        raise create_repo_error(
            code="REPO/EXAM/GET_ANALYSIS",
            message="분석 결과 조회 중 오류가 발생했습니다.",
            cause=e,
        )

def get_analysis_by_school_name(
    db: Session,
    school_name: str,
) -> ExamAnalysis:
    try:
        return db.query(ExamAnalysis).filter(
            ExamAnalysis.school_name == school_name
        ).first()
    except Exception as e:
        raise create_repo_error(
            code="REPO/EXAM/GET_ANALYSIS_BY_SCHOOL",
            message="학교 분석 결과 조회 중 오류가 발생했습니다.",
            cause=e,
        )

def save_exam_result(
    db: Session,
    analysis_id: str,
    exam_content: dict,
) -> ExamResult:
    try:
        exam_result = ExamResult(
            analysis_id=analysis_id,
            exam_content=exam_content,
        )
        db.add(exam_result)
        db.commit()
        db.refresh(exam_result)
        return exam_result
    except Exception as e:
        db.rollback()
        raise create_repo_error(
            code="REPO/EXAM/SAVE_RESULT",
            message="시험지 저장 중 오류가 발생했습니다.",
            cause=e,
        )