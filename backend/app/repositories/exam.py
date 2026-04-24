from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.exam import ExamAnalysis, ExamResult
from app.core.errors import AppError, create_repo_error, map_sqlalchemy_error


# 시험 패턴 분석 결과 저장
async def save_analysis(
    db: AsyncSession,
    school_name: str,
    analysis_result: dict,
) -> ExamAnalysis:
    try:
        analysis = ExamAnalysis(
            school_name=school_name,
            analysis_result=analysis_result,
        )
        db.add(analysis)
        await db.commit()
        await db.refresh(analysis)
        return analysis
    except AppError:
        raise
    except Exception as e:
        await db.rollback()
        raise map_sqlalchemy_error(e, "REPO/EXAM/SAVE_ANALYSIS")


# 시험 패턴 분석 결과 조회
async def get_analysis(
    db: AsyncSession,
    analysis_id: str,
) -> ExamAnalysis:
    try:
        result = await db.execute(
            select(ExamAnalysis).where(ExamAnalysis.id == analysis_id)
        )
        analysis = result.scalar_one_or_none()
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
async def get_analysis_by_school_name(
    db: AsyncSession,
    school_name: str,
) -> Optional[ExamAnalysis]:
    try:
        result = await db.execute(
            select(ExamAnalysis).where(ExamAnalysis.school_name == school_name)
        )
        return result.scalar_one_or_none()
    except AppError:
        raise
    except Exception as e:
        raise map_sqlalchemy_error(e, "REPO/EXAM/GET_ANALYSIS_BY_SCHOOL")


# 시험지 생성 결과 저장
async def save_exam_result(
    db: AsyncSession,
    analysis_id: str,
    exam_content: dict,
) -> ExamResult:
    try:
        exam_result = ExamResult(
            analysis_id=analysis_id,
            exam_content=exam_content,
        )
        db.add(exam_result)
        await db.commit()
        await db.refresh(exam_result)
        return exam_result
    except AppError:
        raise
    except Exception as e:
        await db.rollback()
        raise map_sqlalchemy_error(e, "REPO/EXAM/SAVE_RESULT")


# 시험지 생성 결과 조회
async def get_exam_result(
    db: AsyncSession,
    exam_id: str,
) -> ExamResult:
    try:
        result = await db.execute(
            select(ExamResult).where(ExamResult.id == exam_id)
        )
        exam = result.scalar_one_or_none()
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