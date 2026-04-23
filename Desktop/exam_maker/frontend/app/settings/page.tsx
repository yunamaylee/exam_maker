'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Stepper from '@/components/ui/Stepper'
import { useExamStore } from '@/stores/examStore'

/**
 * 3단계: 문제 설정 페이지
 */
export default function SettingsPage() {
  // hooks
  const router = useRouter()
  const { setOptions, analysisResult } = useExamStore()

  // states
  const [multipleChoice, setMultipleChoice] = useState(
    analysisResult?.exam_meta?.multiple_choice?.count ?? 25
  )
  const [subjective, setSubjective] = useState(
    analysisResult?.exam_meta?.subjective?.count ?? 5
  )
  const [difficulty, setDifficulty] = useState<string | null>(null)

  // handlers
  const handleNext = () => {
    setOptions({
      multiple_choice: multipleChoice,
      subjective,
      difficulty,
    })
    router.push('/result')
  }

  // render
  return (
    <main className="min-h-screen bg-gray-50">
      {/* 헤더 */}
      <header className="bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <img src="/school.png" alt="logo" className="w-8 h-8 rounded-lg" />
          <span className="font-semibold">우리학교출제</span>
        </div>
        <span className="text-xs text-gray-400 border rounded px-2 py-1">Beta</span>
      </header>

      <div className="max-w-2xl mx-auto px-4 py-10 flex flex-col gap-8">
        {/* 스텝퍼 */}
        <Stepper currentStep={3} />

        {/* 본문 */}
        <div className="flex flex-col gap-2">
          <h1 className="text-2xl font-bold">문제 설정</h1>
          <p className="text-gray-500 text-sm">
            문제 수와 난이도를 설정하세요. 설정하지 않으면 학교 기출 유형대로 출제해요.
          </p>
        </div>

        {/* 객관식 문제 수 */}
        <div className="flex flex-col gap-2">
          <label className="text-sm font-medium">객관식 문제 수</label>
          <div className="flex items-center gap-4">
            <input
              type="range"
              min={0}
              max={40}
              value={multipleChoice}
              onChange={(e) => setMultipleChoice(Number(e.target.value))}
              className="flex-1"
            />
            <span className="text-sm font-medium w-12 text-right">{multipleChoice}문제</span>
          </div>
        </div>

        {/* 서술형 문제 수 */}
        <div className="flex flex-col gap-2">
          <label className="text-sm font-medium">서술형 문제 수</label>
          <div className="flex items-center gap-4">
            <input
              type="range"
              min={0}
              max={10}
              value={subjective}
              onChange={(e) => setSubjective(Number(e.target.value))}
              className="flex-1"
            />
            <span className="text-sm font-medium w-12 text-right">{subjective}문제</span>
          </div>
        </div>

        {/* 난이도 */}
        <div className="flex flex-col gap-2">
          <label className="text-sm font-medium">난이도</label>
          <p className="text-xs text-gray-400">선택 안 하면 학교 기출 난이도 그대로 출제해요</p>
          <div className="flex gap-3">
            {['하', '중', '상'].map((level) => (
              <button
                key={level}
                onClick={() => setDifficulty(difficulty === level ? null : level)}
                className={`flex-1 py-3 rounded-xl text-sm font-medium border transition-colors
                  ${difficulty === level
                    ? 'bg-blue-600 text-white border-blue-600'
                    : 'bg-white text-gray-600 border-gray-200 hover:border-blue-300'
                  }`}
              >
                {level}
              </button>
            ))}
          </div>
        </div>

        {/* 다음 버튼 */}
        <button
          onClick={handleNext}
          className="w-full bg-blue-600 text-white py-4 rounded-xl font-semibold transition-colors"
        >
          시험지 생성하기
        </button>
      </div>
    </main>
  )
}