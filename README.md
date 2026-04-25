<div align="center">
  <img width="330" height="250" alt="Image" src="https://github.com/user-attachments/assets/d6438bdb-f501-4123-9047-93e91a78fb44" />
</div>

# 우리학교출제
<div align="center">

학교 기출을 분석해,

학교 선생님의 출제 스타일로,

새로운 시험지를 자동으로 만들어주는 서비스

**[우리학교출제🔗](https://exam-maker-alpha.vercel.app)**

</div>

---
## 서비스 제작 의도

사교육을 다니지 않는 학생들도 
변형문제를 쉽게 얻을 수 있도록 제작하였음.


---

## 서비스 플로우

1. **기출 분석** — 학교 기출 PDF 업로드 → Claude Sonnet으로 출제 패턴 분석

<img width="1000" height="500" alt="Image" src="https://github.com/user-attachments/assets/658867d9-2b49-4931-b9e3-f26b9143c454" />
<br/>
<br/>
<br/>

2. **시험 범위 입력** — 시험 범위 PDF 업로드 (다중 파일) → Claude Haiku로 순수 본문 추출

<img width="1000" height="500" alt="Image" src="https://github.com/user-attachments/assets/45cc9bd2-7fa4-41aa-ab25-3f4225380d47" />
<br/>
<br/>
<br/>
3. **문제 설정** — 문제 수, 난이도, 출제 유형 선택
<img width="1000" height="500" alt="Image" src="https://github.com/user-attachments/assets/6c673c81-8008-4d77-ab4c-10a0c821684d" />
<br/>
<br/>
<br/>
4. **시험지 생성** — Claude Opus로 시험지 생성 → docx 다운로드
<img width="474" height="376" alt="화면 기록 2026-04-24 오후 2 51 34 (1)" src="https://github.com/user-attachments/assets/76362578-4d9e-4c3b-8ea8-9af4a7f7a39b" />

---

## 기술 스택

| Category | Stack |
|----------|-------|
| Backend | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white) |
| Frontend | ![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=nextdotjs&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white) ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat&logo=tailwindcss&logoColor=white) ![Zustand](https://img.shields.io/badge/Zustand-000000?style=flat&logo=react&logoColor=white) |
| AI | ![Claude](https://img.shields.io/badge/Claude_API-D97757?style=flat&logo=anthropic&logoColor=white) |
| Deploy | ![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=flat&logo=railway&logoColor=white) ![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat&logo=vercel&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white) |

---

## 설계 결정

- **Router → Service → Repository** 레이어 분리로 각 역할을 명확히 구분
- - **동일 학교 기출 재업로드 시 DB 조회 캐싱**으로 Claude API 중복 호출 방지 (학교명 기준, 향후 연도별 버전 관리로 확장 가능)
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
