import { create } from 'zustand'

// 타입 정의
type ExamStore = {
  // 1단계: 기출 분석 결과
  analysisId: string | null
  schoolName: string | null
  
  // 2단계: 시험 범위 지문
  passages: object | null
  
  // 3단계: 문제 설정
  options: {
    multiple_choice: number
    subjective: number
    difficulty: string | null
  } | null
  
  // 4단계: 생성된 시험지
  examResult: object | null
  
  // 현재 단계
  currentStep: number

  // actions
  setAnalysisId: (id: string) => void
  setSchoolName: (name: string) => void
  setPassages: (passages: object) => void
  setOptions: (options: ExamStore['options']) => void
  setExamResult: (result: object) => void
  nextStep: () => void
  prevStep: () => void
  reset: () => void
}

export const useExamStore = create<ExamStore>((set) => ({
  // states
  analysisId: null,
  schoolName: null,
  passages: null,
  options: null,
  examResult: null,
  currentStep: 1,

  // actions
  setAnalysisId: (id) => set({ analysisId: id }),
  setSchoolName: (name) => set({ schoolName: name }),
  setPassages: (passages) => set({ passages }),
  setOptions: (options) => set({ options }),
  setExamResult: (result) => set({ examResult: result }),
  nextStep: () => set((state) => ({ currentStep: state.currentStep + 1 })),
  prevStep: () => set((state) => ({ currentStep: state.currentStep - 1 })),
  reset: () => set({
    analysisId: null,
    schoolName: null,
    passages: null,
    options: null,
    examResult: null,
    currentStep: 1,
  }),
}))