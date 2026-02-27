import { cn } from "@/lib/utils"
import { classificationInfo, type Classification } from "@/lib/hospital-data"

interface TriageBadgeProps {
  level: Classification
  showDescription?: boolean
  className?: string
}

export function TriageBadge({ level, showDescription = false, className }: TriageBadgeProps) {
  const info = classificationInfo[level]

  return (
    <div className={cn("flex items-center gap-3", className)}>
      <span className={cn("inline-flex px-3 py-1 rounded-full text-sm font-bold", info.color)}>
        {info.label}
      </span>
      {showDescription && (
        <div>
          <p className="font-semibold">{info.label}</p>
        </div>
      )}
    </div>
  )
}
