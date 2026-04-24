import pypdf
import io
from app.core.errors import AppError, handle_service_error


# PDF 바이트에서 텍스트 추출
def extract_pdf_text(pdf_bytes: bytes) -> str:
    try:
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            text += page_text if page_text else ""
        return text
    except AppError:
        raise
    except Exception as e:
        handle_service_error(
            e,
            code="UTIL/PDF/EXTRACT_TEXT",
            message="PDF 텍스트 추출 중 오류가 발생했습니다.",
        )