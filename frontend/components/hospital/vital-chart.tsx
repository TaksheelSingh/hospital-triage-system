"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from "recharts"

interface VitalData {
  name: string
  value: number
  unit: string
  normalMin: number
  normalMax: number
}

interface VitalChartProps {
  vitals: {
    temperature: number
    pulse: number
    respiration: number
    bpSystolic: number
    bpDiastolic: number
    painScale: number
  }
}

export function VitalChart({ vitals }: VitalChartProps) {
  const data: VitalData[] = [
    { name: "Temp", value: vitals.temperature, unit: "°F", normalMin: 97, normalMax: 99 },
    { name: "Pulse", value: vitals.pulse, unit: "bpm", normalMin: 60, normalMax: 100 },
    { name: "Resp", value: vitals.respiration, unit: "/min", normalMin: 12, normalMax: 20 },
    { name: "BP Sys", value: vitals.bpSystolic, unit: "mmHg", normalMin: 90, normalMax: 120 },
    { name: "BP Dia", value: vitals.bpDiastolic, unit: "mmHg", normalMin: 60, normalMax: 80 },
    { name: "Pain", value: vitals.painScale, unit: "/10", normalMin: 0, normalMax: 3 },
  ]

  const getBarColor = (item: VitalData) => {
    if (item.value < item.normalMin) return "var(--color-chart-2)"
    if (item.value > item.normalMax) return "var(--color-chart-5)"
    return "var(--color-chart-3)"
  }

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-lg">Vitals Visualization</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
              <XAxis dataKey="name" className="text-xs fill-muted-foreground" />
              <YAxis className="text-xs fill-muted-foreground" />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const item = payload[0].payload as VitalData
                    return (
                      <div className="rounded-lg border bg-card p-3 shadow-lg">
                        <p className="font-semibold">{item.name}</p>
                        <p className="text-lg">
                          {item.value}
                          <span className="text-sm text-muted-foreground ml-1">{item.unit}</span>
                        </p>
                        <p className="text-xs text-muted-foreground">
                          Normal: {item.normalMin}-{item.normalMax}
                        </p>
                      </div>
                    )
                  }
                  return null
                }}
              />
              <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getBarColor(entry)} />
                ))}
              </Bar>
              {data.map((item, index) => (
                <ReferenceLine
                  key={`ref-${index}`}
                  y={item.normalMax}
                  stroke="var(--color-muted-foreground)"
                  strokeDasharray="3 3"
                  strokeOpacity={0.3}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-4 flex items-center justify-center gap-6 text-xs">
          <div className="flex items-center gap-2">
            <span className="h-3 w-3 rounded bg-chart-2" />
            <span className="text-muted-foreground">Low</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="h-3 w-3 rounded bg-chart-3" />
            <span className="text-muted-foreground">Normal</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="h-3 w-3 rounded bg-chart-5" />
            <span className="text-muted-foreground">High</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
