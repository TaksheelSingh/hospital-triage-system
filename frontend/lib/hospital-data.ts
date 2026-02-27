export type CaseStatus = "open" | "in-review" | "completed"
export type Classification = "critical" | "needs-review"
export type StaffFormStatus = "idle" | "in-progress" | "submitted"

export interface Prescription {
  id: string
  medicineName: string
  dosage: string
  frequency: string
  discontinued: boolean
  prescribedAt: string
}

export interface Patient {
  id: string
  name: string
  phone: string
  email: string
  age: number
  sex: "male" | "female" | "other"
  dateOfVisit: string
  arrivalMode: string
  arrivalTime: string
  ambulanceTransfer: boolean
  waitTime: number
  status: CaseStatus
  classification: Classification
  riskPercentage: number
  vitals: {
    temperature: number
    pulse: number
    respiration: number
    bpSystolic: number
    bpDiastolic: number
    painScale: number
  }
  rfv1: string
  rfv2?: string
  rfv3?: string
  doctorRemarks?: string
  prescriptions: Prescription[]
}

export const classificationInfo: Record<Classification, { label: string; color: string; bgColor: string }> = {
  critical: { label: "Critical", color: "text-red-600", bgColor: "bg-red-50 border-red-300" },
  "needs-review": { label: "Needs Review", color: "text-green-600", bgColor: "bg-green-50 border-green-300" },
}

export const caseStatusInfo: Record<CaseStatus, { label: string; badgeColor: string }> = {
  open: { label: "Awaiting Doctor Review", badgeColor: "bg-yellow-400 text-black" },
  "in-review": { label: "In Review", badgeColor: "bg-blue-500 text-white" },
  completed: { label: "Completed", badgeColor: "bg-green-600 text-white" },
}

export const staffFormStatusInfo: Record<StaffFormStatus, { label: string; badgeColor: string }> = {
  idle: { label: "Idle", badgeColor: "bg-gray-400 text-white" },
  "in-progress": { label: "In Progress", badgeColor: "bg-yellow-400 text-black" },
  submitted: { label: "Submitted", badgeColor: "bg-green-600 text-white" },
}

export const samplePatients: Patient[] = []
