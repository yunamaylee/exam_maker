# 빌드 스테이지
FROM python:3.9-slim as builder

WORKDIR /app

# 의존성만 먼저 설치 (캐싱 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 실행 스테이지
FROM python:3.9-slim

WORKDIR /app

# 빌드 스테이지에서 설치된 패키지 복사
COPY --from=builder /root/.local /root/.local

# 소스코드 복사
COPY . .

# PATH 설정
ENV PATH=/root/.local/bin:$PATH

# 포트 설정
EXPOSE 8000

# 서버 실행 (마이그레이션 포함)
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]