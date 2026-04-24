import json
import anthropic
from sqlalchemy.orm import Session
from app.core.config import ANTHROPIC_API_KEY
from app.core.errors import AppError, handle_service_error
from app.repositories import exam as exam_repository
from app.prompts.exam import ANALYZE_SCHOOL_PROMPT, EXTRACT_PASSAGES_PROMPT, get_generate_exam_prompt
from app.utils.pdf import extract_pdf_text


def get_anthropic_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


# JSON 코드블록 제거 유틸
def clean_json_response(text: str) -> str:
    return text.replace("```json", "").replace("```", "").strip()


# PDF 바이트에서 텍스트 추출 후 패턴 분석까지 수행 (라우터 진입점)
def analyze_exam_from_pdf(
    db: Session,
    school_name: str,
    pdf_bytes: bytes,
) -> dict:
    try:
        pdf_text = extract_pdf_text(pdf_bytes)
        return analyze_exam_pattern(db=db, school_name=school_name, pdf_text=pdf_text)
    except Aprvice_error(
            e,
            code="SERVICE/EXAM/ANALYZE_FROM_PDF",
            message="PDF 분석 중 오류가 발생했습니다.",
        )


# 시험 범위 PDF에서 지문 추출 (라우터 진입점)
def extract_passages_from_pdf(
    pdf_bytes: bytes,
) -> dict:
    try:
        pdf_text = extract_pdf_text(pdf_bytes)
        return extract_passages(pdf_text=pdf_text)
    except AppError:
        raise
    except Exception as e:
        handle_service_error(
            e,
            code="SERVICE/EXAM/EXTRACT_FROM_PDF",
            message="PDF 지문 추출 중 오류가 발생했습니다.",
        )


# 시험 패턴 분석 함수
def analyze_exam_pattern(
    db: Session,
    school_name: str,
    pdf_text: str,
) -> dict:
    try:
        # DB에 이미 분석 결과 있으면 재활용 (캐싱)
        # 주의: 동일 학교명 기준 캐싱이므로 연도/버전 구분 없음 (의도된 동작)
        existing = exam_repository.get_analysis_by_school_name(
            db=db,           raise ValueError("PDF에서 텍스트를 추출할 수 없습니다.")

        client = get_anthropic_client()

        # Claude Sonnet으로 출제 패턴 분석
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
        analysis_result = json.loads(clean_json_response(message.content[0].text))
        return exam_repository.save_analysis(
            db=db,
            school_name=school_name,
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


# 시험 범???스 예외 발생
        if not pdf_text or not pdf_text.strip():
            raise ValueError("PDF에서 텍스트를 추출할 수 없습니다.")

        client = get_anthropic_client()

        # Claude Haiku로 순수 본문 추출 (듣기 제외)
        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=8000,
            messages=[
                {
                    "role": "user",
                    "content": f"{EXTRACT_PASSAGES_PROMPT}\n\n시험 범위 내용:\n{pdf_text}"
                }
            ]
        )
        return json.loads(clean_json_response(message.content[0].text))
    except AppError:
        raise
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
    optio     analysis_id=analysis_id,
        )

        # 지문이 비어있으면 비즈니스 예외 발생
        if not passages:
            raise ValueError("시험 범위 지문이 없습니다.")

        client = get_anthropic_client()

        # Claude Opus로 시험지 생성
        message = client.messages.create(
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
        exam_content = json.loads(clean_json_response(message.content[0].text))

        # DB 저장
        return exam_repository.save_exam_result(
            db=db,
            analys )
    except AppError:
        raise
    except Exception as e:
        handle_service_error(
            e,
            code="SERVICE/EXAM/GENERATE_EXAM",
            message="시험지 생성 중 오류가 발생했습니다.",
        )


# 시험지 조회 함수
def get_exam(
    db: Session,
    exam_id: str,
) -> dict:
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
