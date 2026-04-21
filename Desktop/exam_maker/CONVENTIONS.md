# 개발 컨벤션

## 원칙

### 단일 책임
- 한 파일, 한 함수는 한 가지 역할만
- 역할이 늘어나면 파일/함수를 나눈다
- 이름만 봐도 뭘 하는지 드러나게 짓는다

### 의존성 최소화
- 레이어 의존 방향은 한 방향만: router → service → repository
- repository가 service를 알면 안 된다

### 가독성 우선
- 성능에 지대한 영향을 주지 않는 한 가독성을 먼저
- 이해하기 쉬운 코드를 유지하는 것을 우선 (AI 활용을 위함)

---

## 프로젝트 구조
app/
├── main.py
├── core/
│   ├── config.py         # 환경변수
│   └── errors.py         # AppError 에러 핸들러
├── routers/              # 엔드포인트만 (얇게 유지)
├── services/             # 비즈니스 로직, repository 조합
├── repositories/         # DB/외부 API 직접 접근만
├── models/               # DB 모델
├── schemas/              # Request/Response Pydantic 타입
└── dependencies.py       # 의존성 주입 (DB 세션 등)

---

## 커밋 메시지

### 형식
타입: 한국어 설명 (#이슈번호)

### 타입
| 타입 | 설명 |
|------|------|
| feat | 새 기능 추가 |
| fix | 버그 수정 |
| refactor | 기능 변화 없이 코드 구조 개선 |
| docs | 문서 수정 |
| chore | 패키지 설치, 설정 파일 변경 |
| test | 테스트 코드 추가 |

### 예시
feat: PDF 업로드 API 추가 (#3)
fix: 시험 범위 벗어난 문제 생성 버그 수정 (#7)
refactor: ExamRepository 단일 책임으로 분리 (#12)
chore: FastAPI 의존성 패키지 설치 (#1)

---

## 브랜치 전략
- main에 직접 커밋하지 않는다
- 이슈 먼저 만들고, 브랜치 판다
- 브랜치 이름: `타입/#이슈번호-간단한설명`
- 예시: `feat/#3-pdf-upload`, `fix/#7-exam-range-bug`

---

## 코드 작성 규칙

### 조건식 - else 쓰지 않는다
```python
# 나쁜 예시
def get_exam(exam_id: str):
    if exam_id:
        return find_exam(exam_id)
    else:
        return None

# 좋은 예시 (early return)
def get_exam(exam_id: str):
    if not exam_id:
        return None
    return find_exam(exam_id)
```

### 함수 - 타입 힌트 필수
```python
# 나쁜 예시
def create_exam(pdf_text, page_range):
    ...

# 좋은 예시
def create_exam(pdf_text: str, page_range: str) -> dict:
    ...
```

### 변수명 - 축약하지 않는다
```python
# 나쁜 예시
d = get_data()
u = get_user()

# 좋은 예시
exam_result = get_exam_result()
current_user = get_user()
```

---

## 에러 핸들링
- 서버는 반드시 에러 핸들러를 가진다
- 에러는 source(어느 레이어), code(어떤 에러), message(설명) 를 포함한다
- repository에서 난 에러와 service에서 난 에러를 구분한다
- 최상단까지 에러가 올라와서 클라이언트에 일관된 메시지를 전달한다