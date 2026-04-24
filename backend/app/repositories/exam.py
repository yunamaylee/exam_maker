from typing import Optional
from sqlalchemy.orm import Session
from app.models.exam import ExamAnalysis, ExamResult
from app.core.errors import AppError, create_repo_error, map_sqlalchemy_error


# 시험 패턴 분석 결과 저장
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
    except AppError:
        raise
    except Exception as e:
        db.rollback()
        raise map_sqlalchemy_error(e, "REPO/EXAM/SAVE_ANALYSIS")


# 시험 패턴 분석 결과 조회
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
    except AppError:
        raise
    except Exception as e:
        raise map_sqlalchemy_error(e, "REPO/EXAM/GET_ANALYSIS")


# 학교명으로 시험 패턴 분석 결과 조회
def get_analysis_by_school_name(
    db: Session,
    school_name: str,
) -> Optional[ExamAnalysis]:
    try:
        return db.query(ExamAnalysis).filter(
            ExamAnalysis.school_name == school_name
        ).first()
    except AppError:
        raise
    except Exception as e:
        raise map_sqlalchemy_error(e, "REPO/EXAM/GET_ANALYSIS_BY_SCHOOL")


# 시험지 생성 결과 저장
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
    except AppError:
        raise
    except Exception as e:
        db.rollback()
        raise map_sqlalchemy_error(e, "REPO/EXAM/SAVE_RESULT")


# 시험지 생성 결과 조회
def get_exam_result(
    db: Session,
    exam_id: str,
) -> ExamResult:
    try:
        exam = db.query(ExamResult).filter(
            ExamResult.id == exam_id
        ).first()
        if not exam:
            raise create_repo_error(
                code="REPO/EXAM/RESULT_NOT_FOUND",
                message="시험지를 찾을 수 없습니다.",
            )
        return exam
    except AppError:
        raise
    except Exception as e:
        raise map_sqlalchemy_error(e, "REPO/EXAM/GET_RESULT")