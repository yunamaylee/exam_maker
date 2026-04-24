# 백엔드 개발 규칙

Python FastAPI 기반 백엔드 개발 규칙입니다.
공통 규칙은 루트 `CONVENTIONS.md`를 참고하세요.

---

## 레이어 구조
router → service → repository

- **router**: 요청 받고 service에 넘기고 응답만 반환. 비즈니스 로직 없음
- **service**: 비즈니스 로직. repository 조합해서 유스케이스 완성
- **repository**: DB 직접 접근만. 단일 동작 단위로

---

## 코드 규칙

- 타입 힌트 필수
- else 쓰지 않고 early return으로
- 변수명 축약하지 않는다
- 함수마다 역할 주석 달기

---

## 에러 핸들링

에러는 source(레이어), code(종류), message(설명)를 담아 최상단까지 올린다.

- repository 에러 → `create_repo_error()`
- service 에러 → `handle_service_error()`
- 최상단 → `main.py`의 `exception_handler`가 잡아서 클라이언트에 반환