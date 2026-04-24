from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime, timezone
import uuid


def utcnow():
    return datetime.now(timezone.utc)


# 시험 분석 모델
class ExamAnalysis(Base):
    __tablename__ = "exam_analysis"
    __table_args__ = (
        UniqueConstraint("school_name", name="uq_exam_analysis_school_name"),
        Index("ix_exam_analysis_school_name", "school_name"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_name = Column(String(100), nullable=False)  # 길이 제한 추가
    analysis_result = Column(JSON, nullable=False)  # 상세 분석 예정으로 JSON 형식 저장
    created_at = Column(DateTime(timezone=True), default=utcnow)

    # 관계 정의
    exam_results = relationship("ExamResult", back_populates="analysis")


# 시험 분석 결과 모델
class ExamResult(Base):
    __tablename__ = "exam_result"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(
        UUID(as_uuid=True),
        ForeignKey("exam_analysis.id", ondelete="CASCADE"),
        nullable=False,
    )
    exam_content = Column(JSON, nullable=False)  # Text → JSON으로 통일
    created_at = Column(DateTime(timezone=True), default=utcnow)

    # 관계 정의
    analysis = relationship("ExamAnalysis", back_populates="exam_results")