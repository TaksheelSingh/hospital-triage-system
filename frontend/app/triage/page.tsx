"use client"

import { useEffect, useState } from "react"
import { Sidebar } from "@/components/hospital/sidebar"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertCircle, CheckCircle, Clock, Users } from "lucide-react"

export default function CaseOverviewPage() {
  const [visits, setVisits] = useState<any[]>([])

  useEffect(() => {
    const fetchVisits = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/visits")
        const data = await res.json()
        setVisits(data)
      } catch (err) {
        console.error("Failed to fetch visits", err)
      }
    }

    fetchVisits()
  }, [])

  const stats = {
    totalVisits: visits.length,
    criticalCases: visits.filter(v => v.classification === "Critical").length,
    needsReviewCases: visits.filter(v => v.classification === "Needs Review").length,
    inReviewCases: visits.filter(v => v.status === "IN_REVIEW").length,
    completedCases: visits.filter(v => v.status === "COMPLETED").length,
  }

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <main className="ml-64 min-h-screen">
        <header className="sticky top-0 z-30 border-b bg-card/80 backdrop-blur-sm">
          <div className="flex h-16 items-center justify-between px-6">
            <div>
              <h1 className="text-2xl font-semibold tracking-tight">📊 Case Overview</h1>
              <p className="text-sm text-muted-foreground">Hospital Operations Dashboard</p>
            </div>
          </div>
        </header>

        <div className="p-6">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5 mb-8">

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
                    <Users className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold">{stats.totalVisits}</p>
                    <p className="text-sm text-muted-foreground">Total Visits</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
                    <AlertCircle className="h-6 w-6 text-red-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-red-600">{stats.criticalCases}</p>
                    <p className="text-sm text-muted-foreground">Critical Cases</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
                    <Clock className="h-6 w-6 text-green-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-green-600">{stats.needsReviewCases}</p>
                    <p className="text-sm text-muted-foreground">Needs Review</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
                    <Clock className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-blue-600">{stats.inReviewCases}</p>
                    <p className="text-sm text-muted-foreground">In Review</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100">
                    <CheckCircle className="h-6 w-6 text-emerald-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-emerald-600">{stats.completedCases}</p>
                    <p className="text-sm text-muted-foreground">Completed Cases</p>
                  </div>
                </div>
              </CardContent>
            </Card>

          </div>
        </div>
      </main>
    </div>
  )
}
