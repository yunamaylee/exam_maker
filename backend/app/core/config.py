from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")

# 필수 환경변수 유효성 검사 - 누락 시 서버 시작 전에 즉시 실패 (fail-fast)
assert DATABASE_URL, "DATABASE_URL 환경변수가 필요합니다."
assert ANTHROPIC_API_KEY, "ANTHROPIC_API_KEY 환경변수가 필요합니다."