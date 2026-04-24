# 코드 작성 규칙

프로젝트 전반에서 아래 규칙을 따릅니다.

---

## 원칙

### 의존성 최소화
- 모듈·파일 간 의존을 줄여서 코드를 빠르게 찾고 수정할 수 있도록 합니다.
- 타입·유틸·훅·상수 등은 사용하는 위치에 두고, 두 곳 이상에서 쓰일 때만 `types/`, `utils/`, `stores/` 등으로 분리합니다.
- 컴포넌트는 재사용 컴포넌트만 추가하며, 불필요하게 컴포넌트화 시키지 않도록 합니다.

### 단일 책임
- 한 파일·한 함수는 한 가지 역할만 담당하도록 하고, 다중 책임을 피합니다.
- 역할이 늘어나면 파일·함수를 나누고, 이름만 봐도 무엇을 하는지 드러나게 짓습니다.

### 가독성 우선
- 성능에 지대한 영향을 주지 않는 경우 가독성을 먼저 합니다.
- 다만, 과도한 재렌더링 등으로 렌더/사이클 파악을 어렵게 만들거나, 레거시가 쌓이는 코드라면 그때는 성능을 먼저 고려합니다.

---

## 프로젝트 구조

### 앱 라우팅 (Next.js App Router)
- `app/` — 페이지 라우팅
- `app/page.tsx` — 1단계: 기출 분석
- `app/range/page.tsx` — 2단계: 시험 범위
- `app/settings/page.tsx` — 3단계: 문제 설정
- `app/result/page.tsx` — 4단계: 시험지 생성
- `app/layout.tsx` — 루트 레이아웃. Provider 래핑

### 경로 별칭

| 별칭 | 디렉터리 | 역할 |
|------|----------|------|
| `@/components/*` | components/ | 재사용 UI 컴포넌트 |
| `@/hooks/*` | hooks/ | 커스텀 훅 |
| `@/stores/*` | stores/ | Zustand 전역 스토어 |
| `@/services/*` | services/ | API 호출 |
| `@/utils/*` | utils/ | 순수 함수 |
| `@/types/*` | types/ | 공용 타입·인터페이스 |
| `@/constants/*` | constants/ | 상수 |

- `types/*`에서 가져온 값은 `import type { ... }` 형태로 씁니다.

---

## 컴포넌트 구조

컴포넌트는 아래 순서의 블록으로 구성합니다. 주석으로 구역을 나눕니다.

### 파일 블록 순서
1. imports
2. constants (이 파일에서만 쓰는 상수)
3. types, interfaces (이 파일에서만 쓰는 타입)
4. root component
5. section components
6. inner components
7. utils

### 컴포넌트 내부 순서

```ts
/**
 * 기출 분석 페이지
 */
const AnalyzePage = () => {
  // hooks
  // states
  // variables
  // functions
  // handlers
  // initialize (useEffect 초기 1회)
  // effects (의존성 useEffect)
  // render
  return (...)
}
```

---

## 성능 관리
- 자식에게 넘기는 핸들러·객체·배열은 필요할 때만 `useCallback`·`useMemo`로 고정합니다.
- props가 바뀌지 않으면 다시 그릴 필요가 없는 자식은 `React.memo`로 감쌉니다.

---

## 상태 관리
- 상태는 필요한 최하위에 둡니다.
- 전역 상태는 **Zustand**를 사용합니다. Context는 테마·인증 등 꼭 필요한 경우에만 씁니다.

---

## 네이밍

### 파일·폴더
- camelCase: `analyzePage.tsx`, `fileUpload.tsx`

### 컴포넌트
- PascalCase + 역할 접미사
- 페이지: `AnalyzePage`
- 섹션: `UploadSection`, `ResultSection`
- 공통: `Stepper`, `FileUpload`, `Button`

### 핸들러
- `handle` + `[대상]` + `[동작]`
- `handleFileUpload`, `handleNextStep`, `handleFormSubmit`

---

## 조건식

else 쓰지 않고 early return으로 분기합니다.

```ts
// 나쁜 예시
if (isLoading) {
  return 
} else {
  return 
}

// 좋은 예시
if (isLoading) return 
return 
```

---

## 함수

### 컴포넌트
파라미터에 타입을 명시해서 선언합니다.

```ts
const Button = ({
  text,
  onClick,
  isDisabled = false,
}: Props) => {
  // ...
}
```

### 유틸·훅
함수 시그니처에 타입만 붙이고, 파라미터 분해는 함수 내부에서 처리합니다.

```ts
type UseStepParams = {
  initialStep?: number
}
export const useStep = (params?: UseStepParams) => {
  const { initialStep = 1 } = params ?? {}
  // ...
}
```

---

## 커밋 메시지

### 형식
타입: 한국어 설명 (#이슈번호)

### 타입
| 타입 | 설명 |
|------|------|
| feat | 새 기능 추가 |
| fix | 버그 수정 |
| refactor | 코드 구조 개선 |
| style | 스타일 수정 |
| docs | 문서 수정 |
| chore | 패키지 설치, 설정 변경 |