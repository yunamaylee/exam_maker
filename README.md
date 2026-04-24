# exam_maker

학교 기출을 분석해 새로운 시험지를 자동으로 만들어주는 서비스

> AI를 활용해 빠르게 구현하되, 설계 원칙을 지키며 확장 가능한 구조로 짭니다.

🔗 **[서비스 바로가기](https://exam-maker-alpha.vercel.app)**

---

## 서비스 플로우

1. **기출 분석** — 학교 기출 PDF 업로드 → Claude Sonnet으로 출제 패턴 분석
2. **시험 범위 입력** — 시험 범위 PDF 업로드 (다중 파일) → Claude Haiku로 순수 본문 추출
3. **문제 설정** — 문제 수, 난이도, 출제 유형 선택
4. **시험지 생성** — Claude Opus로 시험지 생성 → docx 다운로드

---

## 기술 스택

| 영역 | 기술 |
|------|------|
| Backend | Python 3.9, FastAPI, SQLAlchemy, Alembic, PostgreSQL |
| AI | Claude Sonnet (패턴 분석), Haiku (본문 추출), Opus (시험지 생성) |
| Frontend | Next.js, TypeScript, Tailwind CSS, Zustand |
| Deploy | Railway (백엔드 + DB), Vercel (프론트) |

---

## 설계 결정

- **Router → Service → Repository** 레이어 분리로 각 역할을 명확히 구분
- **동일 학교 기출 재업로드 시 DB 캐싱**으로 Claude API 중복 호출 방지
- **단계별 복잡도에 따라 Claude 모델 분리**해 비용과 성능 최적화
- **Dockerfile 멀티스테이지 빌드**로 이미지 크기 최적화
- **서버 시작 시 alembic upgrade head** 자동 실행으로 배포 마이그레이션 자동화

---

## API

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | /api/v1/exam/analyze | 기출 PDF 업로드 및 출제 패턴 분석 |
| POST | /api/v1/exam/range | 시험 범위 PDF 업로드 및 본문 추출 |
| POST | /api/v1/exam/generate | 시험지 생성 |
| GET | /api/v1/exam/{exam_id}/download | 시험지 docx 다운로드 |
| GET | /health | 헬스체크 |

---

## 로컬 실행

```bash
# 백엔드
cd backend
pip install -r requirements.txt
cp .env.example .env  # 환경변수 설정
alembic upgrade head
uvicorn app.main:app --reload

# 프론트엔드
cd frontend
npm install
npm run dev
```

API 문서는 `http://localhost:8000/docs` 에서 확인할 수 있습니다.
