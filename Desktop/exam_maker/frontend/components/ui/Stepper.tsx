// types
type Step = {
  number: number
  label: string
}

type Props = {
  currentStep: number
  steps?: Step[]
}

// constants
const STEP_LIST: Step[] = [
  { number: 1, label: '기출 분석' },
  { number: 2, label: '시험 범위' },
  { number: 3, label: '문제 설정' },
  { number: 4, label: '시험지 생성' },
]

/**
 * 단계 진행 표시
 */
const Stepper = ({ currentStep, steps = STEP_LIST }: Props) => {
  // render
  return (
    <div className="flex items-center justify-center gap-2">
      {steps.map((step, index) => (
        <div key={step.number} className="flex items-center">
          <div className="flex flex-col items-center gap-1">
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold
                ${currentStep >= step.number
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-400'
                }`}
            >
              {step.number}
            </div>
            <span
              className={`text-xs ${
                currentStep === step.number ? 'text-blue-600 font-semibold' : 'text-gray-400'
              }`}
            >
              {step.label}
            </span>
          </div>
          {index < steps.length - 1 && (
            <div
              className={`w-16 h-px mx-2 mb-5 ${
                currentStep > step.number ? 'bg-blue-600' : 'bg-gray-200'
              }`}
            />
          )}
        </div>
      ))}
    </div>
  )
}

export default Stepper