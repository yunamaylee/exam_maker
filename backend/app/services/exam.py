import json
import anthropic
from sqlalchemy.orm import Session
from app.core.config import ANTHROPIC_API_KEY
from app.core.errors import AppError, handle_service_error
from app.repositories import exam as exam_repository
from app.prompts.exam import ANALYZE_SCHOOL_PROMPT, EXTRACT_PASSAGES_PROMPT, get_generate_exam_prompt
from app.utils.pdf import extract_pdf_text
from app.models.exam import ExamAnalysis, ExamResult


def get_anthropic_client() -> anthropic.AsyncAnthropic:
    return anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)


# JSON 코드블록 제거 유틸
def clean_json_response(text: str) -> str:
    return text.replace("```json", "").replace("```", "").strip()


# 학교명 정규화 유틸
# 대소문자, 공백 등 사용자 입력 불일치로 인한 캐시 미스 방지
def normalize_school_name(school_name: str) -> str:
    return school_name.strip()


# Claude API 응답을 JSON으로 안전하게 파싱
# LLM이 JSON이 아닌 응답을 줄 경우 서비스 예외로 변환
def parse_claude_response(text: str, code: str) -> dict:
    try:
        return json.loads(clean_json_response(text))
    except json.JSONDecodeError as e:
        raise AppError(
            source="service",
            code=code,
            message="AI 응답을 파싱하는 중 오류가 발생했습니다.",
            cause=e,
        )


# PDF 바이트에서 텍스트 추출 후 패턴 분석까지 수행 (라우터 진입점)
async def analyze_exam_from_pdf(
    db: Session,
    school_name: str,
    pdf_bytes: bytes,
) -> ExamAnalysis:
    try:
        pdf_text = extract_pdf_text(pdf_bytes)
        return await analyze_exam_pattern(db=db, school_name=school_name, pdf_text=pdf_text)
    except AppError:
        raise
    except Exception as e:
        handle_service_error(
            e,
            code="SERVICE/EXAM/ANALYZE_FROM_PDF",
            message="PDF 분석 중 오류가 발생했습니다.",
        )


# 시험 범위 PDF에서 지문 추출 (라우터 진입점)
async def extract_passages_from_pdf(
    pdf_bytes: bytes,
) -> dict:
    try:
        pdf_text = extract_pdf_text(pdf_bytes)
        return await extract_passages(pdf_text=pdf_text)
    except AppError:
        raise
    except Exception as e:
        handle_service_error(
            e,
            code="SERVICE/EXAM/EXTRACT_FROM_PDF",
            message="PDF 지문 추출 중 오류가 발생했습니다.",
        )


# 시험 패턴 분석 함수
async def analyze_exam_pattern(
    db: Session,
    school_name: str,
    pdf_text: str,
) -> ExamAnalysis:
    try:
        # 학교명 정규화 (공백 제거 등)
        normalized_name = normalize_school_name(school_name)

        # DB에 이미 분석 결과 있으면 재활용
        # 주의: 동일 학교명 기준 캐싱이므로 연도/버전 구분 없음 (의도된 동작)
        existing = exam_repository.get_analysis_by_school_name(
            db=db,
            school_name=normalized_name,
        )
        if existing:
            return existing

        # PDF 텍스트가 비어있으면 비즈니스 예외 발생
        if not pdf_text or not pdf_text.strip():
            raise ValueError("PDF에서 텍스트를 추출할 수 없습니다.")

        client = get_anthropic_client()

        try:
            # Claude Sonnet으로 출제 패턴 분석
            message = await client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": f"{ANALYZE_SCHOOL_PROMPT}\n\n학교명: {normalized_name}\n\n시험지 내용:\n{pdf_text}"
                    }
                ]
            )
        except anthropic.APIError as e:
            raise AppError(
                source="service",
                code="SERVICE/EXAM/CLAUDE_API_ERROR",
                message="AI 서비스 호출 중 오류가 발생했습니다.",
                cause=e,
            )

        analysis_result = parse_claude_response(
            message.content[0].text,
            code="SERVICE/EXAM/ANALYZE_PARSE_ERROR",
        )
        return exam_repository.save_analysis(
            db=db,
            school_name=normalized_name,
            analysis_result=analysis_result,
        )
    except AppError:
        raise
    except Exception as e:
        handle_service_error(
            e,
            code="SERVICE/EXAM/ANALYZE_PATTERN",
            message="시험 패턴 분석 중 오류가 발생했습니다.",
        )


# 시험 범위 본문 추출 함수
async def extract_passages(
    pdf_text: str,
) -> dict:
    try:
        # PDF 텍스트가 비어있으면 비즈니스 예외 발생
        if not pdf_text or not pdf_text.strip():
            raise ValueError("PDF에서 텍스트를 추출할 수 없습니다.")

        client = get_anthropic_client()

        try:
            # Claude Haiku로 순수 본문 추출 (듣기 제외)
            message = await client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=8000,
                messages=[
                    {
                        "role": "user",
                        "content": f"{EXTRACT_PASSAGES_PROMPT}\n\n시험 범위 내용:\n{pdf_text}"
                    }
                ]
            )
        except anthropic.APIError as e:
            raise AppError(
                source="service",
                code="SERVICE/EXAM/CLAUDE_API_ERROR",
                message="AI 서비스 호출 중 오류가 발생했습니다.",
                cause=e,
            )

        return parse_claude_response(
            message.content[0].text,
            code="SERVICE/EXAM/PASSAGES_PARSE_ERROR",
        )
    except AppError:
        raise
    except Exception as e:
        handle_service_error(
            e,
            code="SERVICE/EXAM/EXTRACT_PASSAGES",
            message="시험 범위 본문 추출 중 오류가 발생했습니다.",
        )


# 시험지 생성 함수
async def generate_exam(
    db: Session,
    analysis_id: str,
    passages: dict,
    options: dict,
) -> ExamResult:
    try:
        # 분석 결과 조회
        analysis = exam_repository.get_analysis(
            db=db,
            analysis_id=analysis_id,
        )

        # 지문이 비어있으면 비즈니스 예외 발생
        if not passages:
            raise ValueError("시험 범위 지문이 없습니다.")

        client = get_anthropic_client()

        try:
            # Claude Opus로 시험지 생성
            message = await client.messages.create(
                model="claude-opus-4-5",
                max_tokens=16000,
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
        except anthropic.APIError as e:
            raise AppError(
                source="service",
                code="SERVICE/EXAM/CLAUDE_API_ERROR",
                message="AI 서비스 호출 중 오류가 발생했습니다.",
                cause=e,
            )

        exam_content = parse_claude_response(
            message.content[0].text,
            code="SERVICE/EXAM/GENERATE_PARSE_ERROR",
        )

        # DB 저장
        return exam_repository.save_exam_result(
            db=db,
            analysis_id=str(analysis.id),
            exam_content=exam_content,
        )
    except AppError:
        raise
    except Exception as e:
        handle_service_error(
            e,
            code="SERVICE/EXAM/GENERATE_EXAM",
            message="시험지 생성 중 오류가 발생했습니다.",
        )


# 시험지 조회 함수
async def get_exam(
    db: Session,
    exam_id: str,
) -> ExamResult:
    try:
        return exam_repository.get_exam_result(
            db=db,
            exam_id=exam_id,
        )
    except AppError:
        raise
    except Exception as e:
        handle_service_error(
            e,
            code="SERVICE/EXAM/GET_EXAM",
            message="시험지 조회 중 오류가 발생했습니다.",
        )