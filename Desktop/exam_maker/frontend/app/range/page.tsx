'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Stepper from '@/components/ui/Stepper'
import FileUpload from '@/components/ui/FileUpload'
import { useExamStore } from '@/stores/examStore'
import { extractRange } from '@/services/examService'

/**
 * 2단계: 시험 범위 페이지
 */
export default function RangePage() {
  // hooks
  const router = useRouter()
  const { setPassages } = useExamStore()

  // states
  const [files, setFiles] = useState<File[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // handlers
  const handleFileSelect = (selectedFiles: File[]) => {
    setFiles((prev) => [...prev, ...selectedFiles])
  }

  const handleRemoveFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const handleNext = async () => {
    if (!files.length) return
    setIsLoading(true)
    setError(null)

    try {
      const result = await extractRange({ files })
      setPassages(result.passages)
      router.push('/settings')
    } catch (e) {
      setError('시험 범위 추출 중 오류가 발생했습니다. 다시 시도해주세요.')
    } finally {
      setIsLoading(false)
    }
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
        <Stepper currentStep={2} />

        {/* 본문 */}
        <div className="flex flex-col gap-2">
          <h1 className="text-2xl font-bold">시험 범위 입력</h1>
          <p className="text-gray-500 text-sm">
            시험 범위 PDF를 업로드해주세요. 여러 파일을 올릴 수 있어요.
          </p>
        </div>

        {/* 파일 업로드 */}
        <div className="flex flex-col gap-2">
          <label className="text-sm font-medium">시험 범위 PDF</label>
          <FileUpload
            onFileSelect={handleFileSelect}
            multiple
            description="모의고사, 수능특강, 교과서 등 여러 파일을 올릴 수 있어요"
          />

          {/* 업로드된 파일 목록 */}
          {files.length > 0 && (
            <div className="flex flex-col gap-2 mt-2">
              {files.map((file, index) => (
                <div key={index} className="flex items-center justify-between bg-white border border-gray-200 rounded-lg px-4 py-3">
                  <p className="text-xs text-blue-600">✓ {file.name}</p>
                  <button
                    onClick={() => handleRemoveFile(index)}
                    className="text-xs text-gray-400 hover:text-red-400"
                  >
                    삭제
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 에러 */}
        {error && (
          <p className="text-sm text-red-500">{error}</p>
        )}

        {/* 다음 버튼 */}
        <button
          onClick={handleNext}
          disabled={!files.length || isLoading}
          className="w-full bg-blue-600 text-white py-4 rounded-xl font-semibold disabled:bg-gray-200 disabled:text-gray-400 transition-colors"
        >
          {isLoading ? '분석 중...' : '다음'}
        </button>
      </div>
    </main>
  )
}