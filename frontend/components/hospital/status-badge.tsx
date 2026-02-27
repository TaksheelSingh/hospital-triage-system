import type React from "react"
import { cn } from "@/lib/utils"
import { Clock, RotateCw, CheckCircle } from "lucide-react"
import type { CaseStatus } from "@/lib/hospital-data"

interface StatusBadgeProps {
  status: CaseStatus | string
  className?: string
}

const statusConfig: Record<
  "open" | "in-review" | "completed",
  { label: string; icon: React.ElementType; className: string }
> = {
  open: {
    label: "Awaiting Doctor Review",
    icon: Clock,
    className: "bg-yellow-100 text-yellow-800 border-yellow-300",
  },
  "in-review": {
    label: "In Review",
    icon: RotateCw,
    className: "bg-blue-100 text-blue-800 border-blue-300",
  },
  completed: {
    label: "Completed",
    icon: CheckCircle,
    className: "bg-green-100 text-green-800 border-green-300",
  },
}

export function StatusBadge({ status, className }: StatusBadgeProps) {
  // Normalize backend status (OPEN → open, etc.)
  const normalizedStatus =
    status === "OPEN"
      ? "open"
      : status === "IN_REVIEW"
      ? "in-review"
      : status === "COMPLETED"
      ? "completed"
      : status

  const config = statusConfig[normalizedStatus as keyof typeof statusConfig]

  if (!config) return null

  const Icon = config.icon

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium",
        config.className,
        className
      )}
    >
      <Icon className="h-3.5 w-3.5" />
      {config.label}
    </span>
  )
}