import { Suspense } from "react"
import { PatientsContent } from "@/components/hospital/patients-content"

export default function PatientsPage() {
  return (
    <Suspense fallback={null}>
      <PatientsContent />
    </Suspense>
  )
}
