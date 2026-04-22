from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from datetime import datetime
import uuid

#시험 분석 모델 
class ExamAnalysis(Base):
    __tablename__ = "exam_analysis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_name = Column(String, nullable=False)
    analysis_result = Column(JSON, nullable=False) # 상세 분석 예정으로 JSON 형식 저장 
    created_at = Column(DateTime, default=datetime.utcnow)

# 시험 분석 결과 모델
class ExamResult(Base):
    __tablename__ = "exam_result"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), nullable=False)
    exam_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)