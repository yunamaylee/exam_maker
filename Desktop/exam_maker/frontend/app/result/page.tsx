'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Stepper from '@/components/ui/Stepper'
import { useExamStore } from '@/stores/examStore'
import { generateExam, downloadExam } from '@/services/examService'

/**
 * 4단계: 시험지 생성 페이지
 */
export default function ResultPage() {
  // hooks
  const router = useRouter()
  const { analysisId, passages, options, setExamResult, reset } = useExamStore()

  // states
  const [isLoading, setIsLoading] = useState(true)
  const [examId, setExamId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  // initialize
  useEffect(() => {
    if (!analysisId || !passages || !options) {
      router.push('/')
      return
    }
    handleGenerate()
  }, [])

  // handlers
  const handleGenerate = async () => {
    setIsLoading(true)
    setError(null)
  
    try {
      const result = await generateExam({
        analysisId: analysisId!,
        passages: passages!,
        options: options!,
      })
      setExamResult(result.exam)
      setExamId(result.exam_id)
      // 자동 다운로드 제거
    } catch (e) {
      setError('시험지 생성 중 오류가 발생했습니다. 다시 시도해주세요.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDownload = async () => {
    if (!examId) return
    try {
      await downloadExam({ examId })
    } catch (e) {
      setError('다운로드 중 오류가 발생했습니다.')
    }
  }

  const handleReset = () => {
    reset()
    router.push('/')
  }

  // render
  if (isLoading) {
    return (
      <main className="min-h-screen bg-gray-50 flex flex-col items-center justify-center gap-4">
        <div className="text-4xl animate-spin">⚙️</div>
        <p className="text-gray-500 text-sm">AI가 시험지를 생성하고 다운로드를 준비하고 있어요...</p>
      </main>
    )
  }

  if (error) {
    return (
      <main className="min-h-screen bg-gray-50 flex flex-col items-center justify-center gap-4">
        <p className="text-red-500 text-sm">{error}</p>
        <button
          onClick={handleGenerate}
          className="bg-blue-600 text-white px-6 py-3 rounded-xl text-sm font-medium"
        >
          다시 시도
        </button>
      </main>
    )
  }

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
        <Stepper currentStep={4} />

        {/* 완료 메시지 */}
        <div className="flex flex-col items-center gap-4 py-12">
          <h1 className="text-2xl font-bold">시험지 생성 완료!</h1>
          <p className="text-gray-500 text-sm text-center">
            시험지가 다운로드됐어요. 다시 받고 싶으면 아래 버튼을 눌러요.
          </p>
        </div>

        {/* 에러 */}
        {error && (
          <p className="text-sm text-red-500 text-center">{error}</p>
        )}

        {/* 버튼 */}
        <div className="flex flex-col gap-3">
          <button
            onClick={handleDownload}
            className="w-full bg-blue-600 text-white py-4 rounded-xl font-semibold transition-colors"
          >
            📄 다운로드
          </button>
          <button
            onClick={handleReset}
            className="w-full bg-white text-gray-600 py-4 rounded-xl font-semibold border border-gray-200 transition-colors"
          >
            새 시험지 만들기
          </button>
        </div>
      </div>
    </main>
  )
}