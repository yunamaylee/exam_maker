import { useRef } from 'react'

// types
type Props = {
  onFileSelect: (files: File[]) => void
  multiple?: boolean
  label?: string
  description?: string
}

/**
 * 파일 업로드 컴포넌트
 */
const FileUpload = ({
  onFileSelect,
  multiple = false,
  label = 'PDF 파일을 드래그하거나 클릭하여 업로드',
  description = '학교 내신 시험지 PDF를 올려주세요 (답지 없어도 됩니다)',
}: Props) => {
  // refs
  const inputRef = useRef<HTMLInputElement>(null)

  // handlers
  const handleClick = () => {
    inputRef.current?.click()
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    if (!files.length) return
    onFileSelect(files)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const files = Array.from(e.dataTransfer.files)
    if (!files.length) return
    onFileSelect(files)
  }

  // render
  return (
    <div
      className="border-2 border-dashed border-blue-200 rounded-xl p-12 flex flex-col items-center gap-3 cursor-pointer hover:border-blue-400 transition-colors bg-white"
      onClick={handleClick}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <div className="text-4xl">
        📄
        </div>
      <p className="text-sm text-center">
        <span className="text-blue-600 font-medium">{label}</span>
      </p>
      <p className="text-xs text-gray-400">{description}</p>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        multiple={multiple}
        className="hidden"
        onChange={handleFileChange}
      />
    </div>
  )
}

export default FileUpload