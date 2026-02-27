"use client"

import { useEffect, useState } from "react"
import { Sidebar } from "@/components/hospital/sidebar"
import { StatusBadge } from "@/components/hospital/status-badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Users } from "lucide-react"

export function PatientsContent() {
  const [patients, setPatients] = useState<any[]>([])

  useEffect(() => {
    const fetchPatients = async () => {
      const res = await fetch("http://127.0.0.1:8000/visits")
      const data = await res.json()
      setPatients(data)
    }

    fetchPatients()
  }, [])

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <main className="ml-64 min-h-screen">
        <header className="sticky top-0 z-30 border-b bg-card/80 backdrop-blur-sm">
          <div className="flex h-16 items-center justify-between px-6">
            <div>
              <h1 className="text-2xl font-semibold tracking-tight">Patients</h1>
              <p className="text-sm text-muted-foreground">Live patient records</p>
            </div>
          </div>
        </header>

        <div className="p-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5 text-primary" />
                All Patients ({patients.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              {patients.length === 0 ? (
                <p className="text-center text-muted-foreground py-8">
                  No patients found
                </p>
              ) : (
                <div className="space-y-4">
                  {patients.map((p) => (
                    <div
                      key={p.id}
                      className="flex justify-between rounded-lg border p-4"
                    >
                      <div>
                        <p className="font-semibold">Visit ID: {p.id}</p>
                        <p className="text-sm text-muted-foreground">
                          Status: {p.status}
                        </p>
                      </div>

                      <div>
                        {p.classification && (
                          <p className="font-semibold">
                            {p.classification} (
                            {(p.risk_probability * 100).toFixed(1)}%)
                          </p>
                        )}
                      </div>

                      <StatusBadge status={p.status} />
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}