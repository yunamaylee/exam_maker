# exam_maker

학교 기출을 분석해 새로운 시험지를 자동으로 만들어주는 서비스

> AI를 활용해 빠르게 구현하되, 설계 원칙을 지키며 확장 가능한 구조로 짭니다.

---

## 서비스 소개

<!-- 프론트 완성 후 GIF 추가 예정 -->

원본 지문에서 문제·선택지를 제거하고 순수 본문만 추출한 뒤,
학교 선생님의 출제 패턴을 학습해 새로운 유형으로 문제를 생성합니다.
기존 빈칸을 그대로 재사용하거나 동일한 문제를 내지 않아요.

---

## 기술 스택 & 아키텍처

<!-- 아키텍처 이미지 추가 예정 -->


**설계 결정**
- Router → Service → Repository 레이어 분리로 각 역할을 명확히 구분했습니다
- 동일 학교 기출 재업로드 시 DB 캐싱으로 Claude API 중복 호출을 방지했습니다
- 단계별 복잡도에 따라 Claude 모델을 분리해 비용과 성능을 최적화했습니다
- 향후 AI 모델 교체, 입력 방식 변경 시 Repository만 수정하면 되도록 설계했습니다

---

## 시작하기

1. 의존성 설치
pip install -r requirements.txt

2. 환경 변수 설정
루트에 `.env` 파일을 생성합니다. 필요한 키는 `.env.example`을 참고하세요.

3. DB 설정
alembic upgrade head

4. 서버 실행
uvicorn app.main:app --reload

API 문서는 `http://localhost:8000/docs` 에서 확인할 수 있습니다.

---

## API

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | /api/v1/exam/analyze | 기출 PDF 업로드 및 출제 패턴 분석 |
| POST | /api/v1/exam/range | 시험 범위 PDF 업로드 및 본문 추출 |
| POST | /api/v1/exam/generate | 시험지 생성 |
| GET | /api/v1/exam/{exam_id} | 생성된 시험지 조회 |