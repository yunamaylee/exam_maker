'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Stepper from '@/components/ui/Stepper'
import FileUpload from '@/components/ui/FileUpload'
import { useExamStore } from '@/stores/examStore'
import { analyzeExam } from '@/services/examService'

/**
 * 1단계: 기출 분석 페이지
 */
export default function HomePage() {
  // hooks
  const router = useRouter()
  const { setAnalysisId, setSchoolName, setAnalysisResult } = useExamStore()

  // states
  const [schoolName, setSchoolNameInput] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [localResult, setLocalResult] = useState<any>(null)

  // handlers
  const handleFileSelect = (files: File[]) => {
    setFile(files[0])
  }

  const handleAnalyze = async () => {
    if (!schoolName || !file) return
    setIsLoading(true)
    setError(null)

    try {
      const result = await analyzeExam({ schoolName, file })
      console.log('result:', result)
      console.log('analysis_result:', result.analysis_result)
      setAnalysisId(result.analysis_id)
      setSchoolName(schoolName)
      setAnalysisResult(result.analysis_result)
      setLocalResult(result.analysis_result)
      setShowResult(true)
    } catch (e) {
      setError('분석 중 오류가 발생했습니다. 다시 시도해주세요.')
    } finally {
      setIsLoading(false)
    }
  }

  // render
  return (
    <main className="min-h-screen bg-gray-50">
      {/* 헤더 */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
        <img src="/school.png" alt="logo" className="w-8 h-8 rounded-lg" />
          <span className="font-semibold">우리학교출제</span>
        </div>
        <span className="text-xs text-gray-400 border rounded px-2 py-1">Beta</span>
      </header>

      <div className="max-w-2xl mx-auto px-4 py-10 flex flex-col gap-8">
        {/* 스텝퍼 */}
        <Stepper currentStep={1} />

        {/* 본문 */}
        <div className="flex flex-col gap-2">
          <h1 className="text-2xl font-bold">학교 기출 시험지 업로드</h1>
          <p className="text-gray-500 text-sm">
            학교 기출 시험지를 업로드하면 AI가 출제 유형, 변형 방식, 난이도 패턴을 분석해요.
          </p>
        </div>

        {/* 학교 이름 입력 */}
        <div className="flex flex-col gap-2">
          <label className="text-sm font-medium">학교 이름</label>
          <input
            type="text"
            placeholder="예: 가나다고등학교"
            value={schoolName}
            onChange={(e) => setSchoolNameInput(e.target.value)}
            className="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-400"
          />
        </div>

        {/* 파일 업로드 */}
        <div className="flex flex-col gap-2">
          <label className="text-sm font-medium">기출 시험지 PDF</label>
          <FileUpload
            onFileSelect={handleFileSelect}
            selectedFiles={file ? [file] : []}
            description="학교 내신 시험지 PDF를 올려주세요 (답지 없어도 됩니다)"
          />
        </div>

        {/* 에러 */}
        {error && (
          <p className="text-sm text-red-500">{error}</p>
        )}
        {/* 분석 결과 */}
        {showResult && localResult && (
          <div className="flex flex-col gap-4 bg-blue-50 border border-blue-100 rounded-xl p-6">
            <h2 className="text-base font-semibold text-blue-800">분석 완료</h2>
            <div className="flex flex-col gap-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">전체 문항</span>
                <span className="font-medium">{localResult.exam_meta?.total_questions}문제</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">객관식</span>
                <span className="font-medium">{localResult.exam_meta?.multiple_choice?.count}문제</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">서술형</span>
                <span className="font-medium">{localResult.exam_meta?.subjective?.count}문제</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">난이도</span>
                <span className="font-medium">{localResult.difficulty_analysis?.overall}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">출제 성향</span>
                <span className="font-medium">{localResult.teacher_style?.philosophy}</span>
              </div>
            </div>
            <div className="flex flex-col gap-1">
              <span className="text-xs font-medium text-gray-500">핵심 인사이트</span>
              {localResult.key_insights?.slice(0, 3).map((insight: string, i: number) => (
                <p key={i} className="text-xs text-gray-600">• {insight}</p>
              ))}
            </div>
          </div>
        )}
        {/* 다음 버튼 */}
        <button
        onClick={showResult ? () => router.push('/range') : handleAnalyze}
        disabled={(!schoolName || !file || isLoading) && !showResult}
        className="w-full bg-blue-600 text-white py-4 rounded-xl font-semibold disabled:bg-gray-200 disabled:text-gray-400 transition-colors"
      >
        {isLoading ? '분석 중...' : showResult ? '다음 단계로' : '기출 분석 시작'}
      </button>
      </div>
    </main>
  )
}