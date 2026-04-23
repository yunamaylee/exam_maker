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

  const response = await fetch(
    `${BASE_URL}/api/v1/exam/analyze?school_name=${encodeURIComponent(schoolName)}`,
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