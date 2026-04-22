import pypdf
import io
import json
import anthropic
from sqlalchemy.orm import Session
from app.core.config import ANTHROPIC_API_KEY
from app.core.errors import handle_service_error
from app.repositories import exam as exam_repository
from app.prompts.exam import ANALYZE_SCHOOL_PROMPT, EXTRACT_PASSAGES_PROMPT, get_generate_exam_prompt

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# PDF 텍스트 추출 함수
def extract_pdf_text(pdf_bytes: bytes) -> str:
    try:
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        handle_service_error(
            e,
            code="SERVICE/EXAM/EXTRACT_PDF",
            message="PDF 텍스트 추출 중 오류가 발생했습니다.",
        )

# 시험 패턴 분석 함수
def analyze_exam_pattern(
    db: Session,
    school_name: str,
    pdf_text: str,
) -> dict:
    try:
        # DB에 이미 분석 결과 있으면 재활용
        existing = exam_repository.get_analysis_by_school_name(
            db=db,
            school_name=school_name,
        )
        if existing:
            return existing

        # 없으면 Claude API 호출
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": f"{ANALYZE_SCHOOL_PROMPT}\n\n학교명: {school_name}\n\n시험지 내용:\n{pdf_text}"
                }
            ]
        )
        analysis_result = json.loads(message.content[0].text)
        return exam_repository.save_analysis(
            db=db,
            school_name=school_name,
            analysis_result=analysis_result,
        )
    except Exception as e:
        handle_service_error(
            e,
            code="SERVICE/EXAM/ANALYZE_PATTERN",
            message="시험 패턴 분석 중 오류가 발생했습니다.",
        )


# 시험 범위 본문 추출 함수
def extract_passages(
    pdf_text: str,
) -> dict:
    try:
        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": f"{EXTRACT_PASSAGES_PROMPT}\n\n시험 범위 내용:\n{pdf_text}"
                }
            ]
        )
        return json.loads(message.content[0].text)
    except Exception as e:
        handle_service_error(
            e,
            code="SERVICE/EXAM/EXTRACT_PASSAGES",
            message="시험 범위 본문 추출 중 오류가 발생했습니다.",
        )


# 시험지 생성 함수
def generate_exam(
    db: Session,
    analysis_id: str,
    passages: dict,
    options: dict,
) -> dict:
    try:
        # 분석 결과 조회
        analysis = exam_repository.get_analysis(
            db=db,
            analysis_id=analysis_id,
        )

        # 시험지 생성
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": get_generate_exam_prompt(
                        school_profile=json.dumps(analysis.analysis_result, ensure_ascii=False),
                        passages=json.dumps(passages, ensure_ascii=False),
                        options=json.dumps(options, ensure_ascii=False),
                    )
                }
            ]
        )

        exam_content = json.loads(message.content[0].text)

        # DB 저장
        return exam_repository.save_exam_result(
            db=db,
            analysis_id=str(analysis.id),
            exam_content=exam_content,
        )
    except Exception as e:
        handle_service_error(
            e,
            code="SERVICE/EXAM/GENERATE_EXAM",
            message="시험지 생성 중 오류가 발생했습니다.",
        )