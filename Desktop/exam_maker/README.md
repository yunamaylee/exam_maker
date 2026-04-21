# exam_maker

학교 기출 PDF를 분석해 새로운 시험지를 자동 생성하는 서비스

## 왜 만들었나
기존 시험지 생성 도구는 원본 문제를 그대로 재활용해요.
exam_maker는 원본 지문에서 문제/선택지를 제거하고,
순수 본문만 추출해 학교 출제 유형에 맞는 새 문제를 생성해요.

## 설계 원칙
이 프로젝트는 기능 구현보다 확장 가능한 구조 설계에 집중했습니다.
AI 모델 교체, 입력 방식 변경 등 요구사항이 바뀌어도
핵심 비즈니스 로직은 건드리지 않아도 되는 구조를 목표로 했습니다.

## 프로젝트 구조
app/
├── main.py
├── core/
│   ├── config.py         # 환경변수
│   └── errors.py         # 에러 핸들러
├── routers/              # 엔드포인트
├── services/             # 비즈니스 로직
├── repositories/         # DB/외부 API 접근
├── models/               # DB 모델
├── schemas/              # Request/Response 타입
└── dependencies.py       # 의존성 주입

## 시작하기

1. 의존성 설치
pip install -r requirements.txt

2. 환경 변수 설정
루트에 .env 파일을 생성합니다.
필요한 키 값은 .env.example을 참고하세요.

3. 개발 서버 실행
uvicorn app.main:app --reload

## 기술 스택
- Python, FastAPI
- PostgreSQL
- OpenAI API