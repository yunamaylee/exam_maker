import anthropic
from sqlalchemy.orm import Session
from app.core.config import ANTHROPIC_API_KEY
from app.core.errors import handle_service_error
from app.repositories import exam as exam_repository
from app.repositories import exam as exam_repository


client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def extract_pdf_text(pdf_bytes: bytes) -> str:
    try:
        import pypdf
        import io
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