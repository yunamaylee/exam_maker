const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// 기출 PDF 분석
export async function analyzeExam({
  schoolName,
  file,
}: {
  schoolName: string
  file: File
}) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('school_name', schoolName)  // query parameter → form data로 변경

  const response = await fetch(
    `${BASE_URL}/api/v1/exam/analyze`,  // query string 제거
    {
      method: 'POST',
      body: formData,
    }
  )

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.message)
  }

  return response.json()
}

// 시험 범위 본문 추출
export async function extractRange({
  files,
}: {
  files: File[]
}) {
  const formData = new FormData()
  files.forEach((file) => formData.append('files', file))

  const response = await fetch(`${BASE_URL}/api/v1/exam/range`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.message)
  }

  return response.json()
}

// 시험지 생성
export async function generateExam({
  analysisId,
  passages,
  options,
}: {
  analysisId: string
  passages: object
  options: object
}) {
  const response = await fetch(
    `${BASE_URL}/api/v1/exam/generate?analysis_id=${analysisId}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ passages, options }),
    }
  )

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.message)
  }

  return response.json()
}

// 시험지 docx 다운로드
export async function downloadExam({ examId }: { examId: string }) {
  const response = await fetch(`${BASE_URL}/api/v1/exam/${examId}/download`)
  
  if (!response.ok) throw new Error('다운로드 실패')
  
  const blob = await response.blob()
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `시험지_${examId}.docx`
  a.click()
  window.URL.revokeObjectURL(url)
}