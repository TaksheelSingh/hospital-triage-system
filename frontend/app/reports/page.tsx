"use client"

import { Sidebar } from "@/components/hospital/sidebar"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { FileText, Download, Calendar, BarChart3 } from "lucide-react"

export default function ReportsPage() {
  const reports = [
    { name: "Daily Patient Summary", date: "2026-01-11", type: "Daily" },
    { name: "Weekly Triage Analysis", date: "2026-01-10", type: "Weekly" },
    { name: "Monthly Performance Report", date: "2026-01-01", type: "Monthly" },
    { name: "Emergency Department Metrics", date: "2026-01-11", type: "Real-time" },
  ]

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <main className="ml-64 min-h-screen">
        <header className="sticky top-0 z-30 border-b bg-card/80 backdrop-blur-sm">
          <div className="flex h-16 items-center justify-between px-6">
            <div>
              <h1 className="text-2xl font-semibold tracking-tight">Reports</h1>
              <p className="text-sm text-muted-foreground">Analytics and documentation</p>
            </div>
            <Button>
              <FileText className="mr-2 h-4 w-4" />
              Generate Report
            </Button>
          </div>
        </header>

        <div className="p-6">
          <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <Card className="cursor-pointer transition-colors hover:bg-muted/50">
              <CardContent className="flex items-center gap-4 p-6">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                  <Calendar className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <p className="font-semibold">Daily Reports</p>
                  <p className="text-sm text-muted-foreground">Patient intake summaries</p>
                </div>
              </CardContent>
            </Card>
            <Card className="cursor-pointer transition-colors hover:bg-muted/50">
              <CardContent className="flex items-center gap-4 p-6">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-accent/10">
                  <BarChart3 className="h-6 w-6 text-accent" />
                </div>
                <div>
                  <p className="font-semibold">Analytics</p>
                  <p className="text-sm text-muted-foreground">Triage and performance</p>
                </div>
              </CardContent>
            </Card>
            <Card className="cursor-pointer transition-colors hover:bg-muted/50">
              <CardContent className="flex items-center gap-4 p-6">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-triage-routine/10">
                  <FileText className="h-6 w-6 text-triage-routine" />
                </div>
                <div>
                  <p className="font-semibold">Custom Reports</p>
                  <p className="text-sm text-muted-foreground">Build your own report</p>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Recent Reports</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {reports.map((report, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between rounded-lg border p-4 transition-colors hover:bg-muted/50"
                  >
                    <div className="flex items-center gap-4">
                      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-muted">
                        <FileText className="h-5 w-5 text-muted-foreground" />
                      </div>
                      <div>
                        <p className="font-medium">{report.name}</p>
                        <p className="text-sm text-muted-foreground">
                          {report.date} • {report.type}
                        </p>
                      </div>
                    </div>
                    <Button variant="ghost" size="icon">
                      <Download className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
